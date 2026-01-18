import stripe, time
from botocore.exceptions import ClientError

from django.shortcuts import (
    render, 
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import (
    RedirectView, 
    TemplateView,
    ListView,
)
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    Http404,  
    HttpResponseForbidden,
    HttpResponse,
)
from django.utils.translation import ugettext_lazy as _, get_language
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.db.models import Q

from logging import getLogger

from hitcount.views import (
    HitCountDetailView,
)

from diventi.core.views import DiventiActionMixin
from diventi.core.utils import (
    humanize_price,
)
from diventi.ebooks.models import (
    Book
)
from diventi.geminigm.models import GemmaIstruction

from .models import (
    Product,
    ProductCategory,
    ProductCover,
    ProductDownloadSession,
)
from .forms import UserCollectionUpdateForm
from .utils import (
    add_product_to_user_collection,
    get_s3_safe_url,
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
        products = Product.objects.published().order_by('-publication_date')
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

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListViewByCategory, self).get_context_data(*args, **kwargs)
        filtered_category = get_object_or_404(ProductCategory, slug=self.kwargs['category'])
        context['filtered_category'] = filtered_category
        return context


class ProductDetailView(HitCountDetailView):
    """
        Renders the product contents.
    """
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail_quick.html'
    count_hit = True

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
        context['latest_articles'] = self.object.related_articles.all().order_by('-publication_date')[:3]
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
        ebook = Book.objects.filter(book_product=product).first()
        gemma = GemmaIstruction.objects.filter(gemma_product=product).first()
        if gemma:
            return reverse('geminigm:gemma_public', kwargs={'gemma_slug': gemma.slug})
        elif ebook.paper_id or ebook.legacy_paper_id:
            return reverse('ebooks:book-detail-public', kwargs={'book_slug': ebook.slug})
        elif ebook.content_file_url:
            return reverse('ebooks:pdf-detail-public', kwargs={'book_slug': ebook.slug})
        else:
            msg = _('This product has no content attached, please contact the authors.')
            raise Http404(msg) 


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


class CheckoutDoneTemplateView(TemplateView):

    template_name = 'products/checkout_done_quick.html'


class CheckoutFailedTemplateView(TemplateView):

    template_name = 'products/checkout_failed_quick.html'


def checkout_done_pdf(request, slug, session_id):
    # Configurazione validità
    VALIDITY_MINUTES = 15

    try:
        product = Product.objects.get(
            Q(slug_it=slug) | Q(slug_en=slug)
        )
    except Product.DoesNotExist:    
        return HttpResponseForbidden(_('Product not found'))
    except NameError:
        return HttpResponseForbidden(_('Server Error: Product model not imported'))

    if not session_id:
        return HttpResponseForbidden(_("The link is not valid."))

    if product.user_has_already_bought(request.user):
        return redirect(reverse('products:user_product_download', kwargs=({'slug': slug,})))

    # A. VERIFICA DATABASE (Il controllo più veloce e sicuro)
    # Cerchiamo se questo session_id è già stato usato in passato.
    download_record = ProductDownloadSession.objects.filter(session_id=session_id).first()

    if download_record:
        # Il link è già stato usato!
        # Controlliamo se è ancora valido
        if not download_record.is_valid(validity_minutes=VALIDITY_MINUTES):            
            return HttpResponseForbidden(_("Download link expired. To retrieve it, please log in to your reserved area or contact the authors."))
        
        # Se siamo qui, il timer è ancora buono. Procediamo.
        customer_email = download_record.stripe_email

    else:
        # B. PRIMO ACCESSO ASSOLUTO
        # Se non esiste nel DB, dobbiamo validare con Stripe (costoso ma necessario una tantum)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception:
            return HttpResponseForbidden(_("The stripe session is not valid."))

        if session.payment_status != 'paid':
            return HttpResponseForbidden(_("The payment has not been fulfilled."))

        # RECUPERO EMAIL DA STRIPE
        # L'email si trova solitamente in customer_details
        if session.customer_details and session.customer_details.email:
            customer_email = session.customer_details.email
        else:
            # Fallback per vecchie versioni API o casi specifici
            customer_email = session.customer_email

        # C. REGISTRAZIONE NEL DATABASE
        ProductDownloadSession.objects.create(
            session_id = session_id,
            user = request.user if request.user.is_authenticated else None,
            stripe_email = customer_email,
            product = product,
        )
    
    # Logica business utente loggato (aggiungi a libreria)
    if request.user.is_authenticated:
        try:
            add_product_to_user_collection(product, user=request.user)
        except Http404:
            pass

    # --- D1. PAGINA DI OK IN CASO DI PRODOTTO WEB ---
    if hasattr(product, 'book'):
        return redirect(reverse('products:checkout_done', kwargs={'slug': slug}))
    else:
        # --- D2. GENERAZIONE PRESIGNED URL S3 IN CASO DI PRODOTTO FILE ---
        response_url = get_s3_safe_url(product)
        return render(request, 'products/checkout_done_pdf.html', {
            'response_url': response_url,
        })


@login_required
def user_product_download(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if product.user_has_already_bought(request.user) or product.user_has_authored(request.user):
        response_url = get_s3_safe_url(product)
        return render(request, 'products/checkout_done_pdf.html', {
            'response_url': response_url,
        })
    else:
        return HttpResponseForbidden(_("This product in not in your collection."))


