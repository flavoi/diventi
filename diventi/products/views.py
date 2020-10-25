import stripe

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import RedirectView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpResponse,
    Http404, 
    HttpResponseGone, 
    HttpResponsePermanentRedirect, 
    HttpResponseRedirect,
)
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from boto.s3.connection import S3Connection
from logging import getLogger

from diventi.core.views import DiventiActionMixin

from .models import Product
from .forms import UserCollectionUpdateForm
from .utils import (
    add_product_to_user_collection,
    humanize_price,
)


class ProductDetailView(DetailView):
    """
        Displays a product with all its infos.
    """
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail_quick.html'

    # Returns only published products
    def get_queryset(self):
        qs = super(ProductDetailView, self).get_queryset()
        return qs.published()

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        context['add_collection_form'] = UserCollectionUpdateForm(initial={'slug': self.object.slug })
        context['drop_collection_form'] = UserCollectionUpdateForm(initial={'slug': self.object.slug })
        context['bought'] = self.object.user_has_already_bought(user)        
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['featured_detail'] = self.object.details.highlighted_or_first()
        if self.object.at_a_premium:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_price = stripe.Price.retrieve(self.object.stripe_price)
            context['price'] = humanize_price(float(stripe_price['unit_amount_decimal']))
        if user.is_authenticated and self.object.product_survey:
            context['survey_answered'] = self.object.product_survey.user_has_answered(user)
        return context


class ProductUpdateView(LoginRequiredMixin, DiventiActionMixin, UpdateView):
    """
        Base update view for the product model
    """
    model = Product
    context_object_name = 'product'


class FreeProductMixin:
    """ Restrict the update to free products only. """

    def post(self, request, *args, **kwargs):        
        if not self.get_object().at_a_premium:
            return super().post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class AddToUserCollectionView(FreeProductMixin, ProductUpdateView):
    """
        Adds a user to the buyers of a product.
    """
    form_class = UserCollectionUpdateForm
    success_msg = _('This item has been added to you collection')
    template_name = 'products/product_detail_quick.html'


    def form_valid(self, form):
        add_product_to_user_collection(self.object, self.request.user)
        return super(AddToUserCollectionView, self).form_valid(form)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        if self.object.user_has_already_bought(self.request.user):
            msg = _('The user has this product already.')
            raise Http404(msg)
        return super().get_initial()


class DropFromUserCollectionView(ProductUpdateView):
    """
        Remove a user to the buyers of a product.
    """
    form_class = UserCollectionUpdateForm
    success_msg = _('This product has been dropped from your collection')
    template_name = 'products/product_detail_quick.html'

    def drop_from_user_collection(self):
        if self.object.user_has_already_bought(self.request.user):
            return self.object.buyers.remove(self.request.user)
        else:
            msg = _("The user hasn't got this product already.")
            raise Http404(msg)

    def form_valid(self, form):
        self.drop_from_user_collection()
        return super(DropFromUserCollectionView, self).form_valid(form)


# Enables logging of failed requests of a file
logger = getLogger('django.request')


class SecretFileView(RedirectView):
    """ Returns a temporary url if the user has added the product to his collection """
    permanent = False

    def get_redirect_url(self, **kwargs):
        s3 = S3Connection(settings.AWS_ACCESS_KEY_ID,
                            settings.AWS_SECRET_ACCESS_KEY,
                            is_secure=True)
        # Create a URL valid for 60 seconds.
        return s3.generate_url(60, 'GET',
                            bucket=settings.AWS_STORAGE_BUCKET_NAME,
                            key=kwargs['filepath'],
                            force_http=True)

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        u = request.user

        if (product.user_has_already_bought(u) or product.user_has_authored(u)) and product.available:
            if product.file:
                filepath = settings.MEDIA_ROOT + product.file.name
                url = self.get_redirect_url(filepath=filepath)
                # The below is taken straight from RedirectView.
                if url:
                    if self.permanent:
                        return HttpResponsePermanentRedirect(url)
                    else:
                        return HttpResponseRedirect(url)
                else:
                    logger.warning('Gone: %s', self.request.path,
                                extra={
                                    'status_code': 410,
                                    'request': self.request
                                })
                    return HttpResponseGone()
            else:
                raise Http404
        else:
            raise Http404


# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY

# You can find your endpoint's secret in your webhook settings
endpoint_secret = 'whsec_NoUa3aBmRfbFvcr8w4fogFf2WfKwGw3E'

@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    item = stripe.checkout.Session.list_line_items(session['id'], limit=1)['data'][0]
    user = get_object_or_404(
        get_user_model(), 
        nametag = session['client_reference_id'],
    )
    product = get_object_or_404(
        Product, 
        stripe_product=item['price']['product'],
    )
    translation.activate(user.language)
    request.LANGUAGE_CODE = translation.get_language()
    add_product_to_user_collection(product, user)
    price = humanize_price(float(session['amount_total']))
    send_mail(
        _('Diventi: %(title)s purchase') % {'title': product.title,},
        _('Dear %(user)s, you have successufully purchased %(title)s for %(price)s.') % {
            'user': user.first_name,
            'price': price,
            'title': product.title,
        },
        'info@playdiventi.it',
        [user.email],
        fail_silently=False,
    )
  return HttpResponse(status=200)


class CheckoutDoneTemplateView(TemplateView):

    template_name = 'products/checkout_done_quick.html'


class CheckoutFailedTemplateView(TemplateView):

    template_name = 'products/checkout_failed_quick.html'

        
