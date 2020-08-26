import stripe

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import RedirectView
from django.http import Http404, HttpResponseGone, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import messages

from boto.s3.connection import S3Connection
from logging import getLogger

from diventi.core.views import DiventiActionMixin
from diventi.payments.views import charge

from .models import Product
from .forms import UserCollectionUpdateForm

# Paymens api
stripe.api_key = settings.STRIPE_SECRET_KEY


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
        return context


class ProductUpdateView(LoginRequiredMixin, DiventiActionMixin, UpdateView):
    """
        Base update view for the product model
    """
    model = Product
    context_object_name = 'product'


class AddToUserCollectionView(ProductUpdateView):
    """
        Adds a user to the buyers of a product.
    """
    form_class = UserCollectionUpdateForm
    success_msg = _('This product has been added to you collection')
    template_name = 'products/product_detail_quick.html'

    def add_to_user_collection(self, user):
        if not self.object.user_has_already_bought(user):
            if self.object.price > 0:
                payment = charge(self.request, self.object.price, self.object.title, user)
                msg = payment['msg']
                if payment['outcome'] != 1: # Failed charge
                    raise Http404(msg)
                else:
                    messages.add_message(self.request, messages.INFO, msg)
            return self.object.customers.add(user)
        else:
            msg = _('The user has this product already.')
            raise Http404(msg)

    def form_valid(self, form):
        self.add_to_user_collection(self.request.user)
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
