import stripe

from django.shortcuts import (
    render, 
    get_object_or_404,
    redirect,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import (
    RedirectView, 
    TemplateView,
    ListView,
)
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
from django.urls import reverse
from django.shortcuts import (
    render,
    redirect
)

from boto.s3.connection import S3Connection
from logging import getLogger

from diventi.core.views import DiventiActionMixin

from .models import (
    Product,
    ProductCategory,
    ProductCover,
)

from diventi.ebooks.models import (
    Book
)

from .forms import UserCollectionUpdateForm
from .utils import (
    add_product_to_user_collection,
    humanize_price,
)


class ProductListView(ListView):
    """
        Displays the list of published products.
    """
    model = Product
    template_name = 'products/product_list_quick.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        products = Product.objects.published().order_by('publication_date')
        products = products.exclude(category__meta_category=True)
        return products

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['categories'] = ProductCategory.objects.visible()
        context['hot_products'] = (Product.objects.hot() | Product.objects.pinned_list()).distinct()
        context['productcover'] = ProductCover.objects.active()
        return context


class ProductListViewByCategory(ProductListView):
    """
        Display a filtered list of published products by a selected category.
    """

    template_name = 'products/product_list_filtered_quick.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.category(category_slug=self.kwargs['category'])


class ProductDetailView(DetailView):
    """
        Renders the product contents.
    """
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail_quick.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.public: 
            return redirect('products:detail-public', slug=obj.slug)
        return super().get(request, *args, **kwargs)

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
        context['featured_detail'] = self.object.details.highlighted_or_first()
        if self.object.at_a_premium:            
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_price = stripe.Price.retrieve(self.object.stripe_price)
            context['price'] = humanize_price(float(stripe_price['unit_amount_decimal']))
            context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
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


class PublicProductMixin:
    """ Restrict the access to public products only. """

    def post(self, request, *args, **kwargs):
        obj =  self.get_object()  
        if not obj.public:
            return super().post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PublishedProductMixin:
    """ Restrict the access to public products only. """

    def post(self, request, *args, **kwargs):
        obj =  self.get_object()  
        if not obj.published:
            return super().post(request, *args, **kwargs)
        else:
            raise PermissionDenied


class RedirectToPublicEbookView(PublishedProductMixin, PublicProductMixin, RedirectView):
    
    def get_redirect_url(self, **kwargs):
        product = get_object_or_404(Product, slug=kwargs.get('slug'))
        ebook = get_object_or_404(Book, book_product=product)
        return reverse('ebooks:book-detail-public', kwargs={'book_slug': ebook.slug})


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


def add_public_product_to_user_collection_view(request, slug):
    """
        Add the selected product to the user collection and the return to the caller page.
        If the prodct is not public it doesn't do anything.
    """

    product = get_object_or_404(Product, slug=slug)
    if product.public:
        add_product_to_user_collection(product, request.user)
        message = _('%(p)s has been added in your collection.') % {
            'p': product.title,
        }
        messages.add_message(request, messages.SUCCESS, message)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    messages.add_message(request, messages.WARNING, _('The requested product is not public.'))
    return redirect(product)


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


class CheckoutDoneTemplateView(TemplateView):

    template_name = 'products/checkout_done_quick.html'


class CheckoutFailedTemplateView(TemplateView):

    template_name = 'products/checkout_failed_quick.html'

        
