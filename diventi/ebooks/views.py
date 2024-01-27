from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views import View
from django.utils.translation import (
    get_language,
    gettext_lazy as _
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin,
    AccessMixin,
)
from django.http import (
    Http404, 
    HttpResponseRedirect,
)
from django.core.exceptions import PermissionDenied

from hitcount.models import HitCount
from hitcount.views import (
    HitCountMixin, 
    HitCountDetailView,
)

from diventi.products.models import Product

from .models import Book

from .utils import (
    get_paper_filename,
    parse_paper_soup,
    make_paper_toc,
)


class UserHasProductMixin(UserPassesTestMixin):
    """ 
        This view checks if the user has bought the product
        related to the requested book. 
        It assumes to have the slug of the book object available
        in book_slug get parameter.
    """

    permission_denied_message = _('This book is not in your collection, please check your profile.')

    def test_func(self):
        book_slug = self.kwargs.get('book_slug', None)
        book = get_object_or_404(Book, slug=book_slug)
        product = book.book_product
        user_has_bought_test = product.user_has_already_bought(self.request.user) or product.user_has_authored(self.request.user)
        if not user_has_bought_test:
            self.permission_denied_message = _('This book is not in your collection, please check your profile.')        
        return user_has_bought_test 


class BookIsPublishedMixin(UserPassesTestMixin):
    """
        This view checks if the book has been published.
        It assumes to have the slug of the book object available
        in book_slug get parameter.
    """
    def test_func(self):        
        book_slug = self.kwargs.get('book_slug', None)
        book = get_object_or_404(Book, slug=book_slug)
        book_is_published_test = book.is_published()
        if not book_is_published_test:
            self.permission_denied_message = _('This book is not published yet, please check back later.')
        return book_is_published_test


class PublicEbookMixin(UserPassesTestMixin):
    """
        Returns the ebook if the product is public, or else it redirects to the default view.
    """
    def test_func(self):
        book_slug = self.kwargs.get('book_slug', None)
        book = get_object_or_404(Book, slug=book_slug)
        product = get_object_or_404(Product, id=book.book_product.id)
        book_is_public_test = product.public
        if not book_is_public_test:
            self.permission_denied_message = _("This book has no content attached, please contact the authors.")
        return book_is_public_test


class EbookView(View):
    """ 
        Generic view that manages context data for ebooks. 
        It assumes to have the slug of the book object available
        in book_slug get parameter.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_slug = self.kwargs.get('book_slug', None)
        book = get_object_or_404(Book, slug=book_slug)
        context['book'] = book
        return context


class BookDetailView(EbookView, HitCountDetailView):
    """ Returns the digital content of a product. """
    
    model = Book
    slug_url_kwarg = 'book_slug'
    count_hit = True

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.published().product()

    def get_template_names(self):
        return ['ebooks/book_detail_quick.html', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bought'] = self.object.book_product.user_has_already_bought(self.request.user)
        return context


class PaperEbookView(BookIsPublishedMixin, BookDetailView):
    """ Renders an ebook from a paper document """
   
    def get_object(self, queryset=None):
        obj = super(PaperEbookView, self).get_object(queryset)
        if not obj.paper_id:
            raise Http404(_('This book is not linked to a paper, please contact the authors.'))
        return obj

    def get_template_names(self):
        return ['ebooks/book_detail_quick.html', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_lan = self.kwargs.get('language_code')
        if not current_lan:
            current_lan = get_language()        
        context['authored'] = self.object.book_product.user_has_authored(self.request.user)
        paper_filename = get_paper_filename(paper_id=self.object.id, paper_lan=current_lan)
        paper_soup = parse_paper_soup(paper_filename)
        context['paper_title'] = self.object.title
        context['paper_toc'] = make_paper_toc(paper_soup)
        context['book_paper'] = paper_filename
        context['current_lan'] = current_lan
        return context


class PublicPaperEbookView(PublicEbookMixin, PaperEbookView):
    """
        Renders the ebook regardless of the user or their collection.
    """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = self.object.book_product.related_products.all()
        context['related_products'] = related_products
        return context


class PrivatePaperEbookView(LoginRequiredMixin, UserHasProductMixin, PaperEbookView):
    """
        Renders the ebook if and only if the user is authenticated 
        and has the product in their collection.
    """
    pass


class PdfEbookView(BookIsPublishedMixin, BookDetailView):
    """ Returns the pdf url of the ebook """

    def get_template_names(self):
        return ['ebooks/book_detail_pdf.html', ]


class PublicPdfEbookView(PublicEbookMixin, PdfEbookView):
    """
        Renders the ebook regardless of the user or their collection.
    """
    pass


class PrivatePdfEbookView(LoginRequiredMixin, UserHasProductMixin, PdfEbookView):
    """
        Renders the ebook if and only if the user is authenticated 
        and has the product in their collection.
    """
    pass







