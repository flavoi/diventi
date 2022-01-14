from django.shortcuts import (
    get_object_or_404,
    redirect,
) 

from django.views.generic.detail import DetailView
from django.views import View
from django.utils.translation import (
    get_language,
    gettext_lazy as _
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)
from django.http import Http404
from django.conf import settings

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
        book_is_published_test = book.is_published()
        if not book_is_published_test:
            self.permission_denied_message = _('This book is not yet available, please check back later.')
        return user_has_bought_test and book_is_published_test


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


class PublicEbookMixin:
    """
        Returns the ebook if the product is public, or else it redirects to the default view.
    """
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        product = get_object_or_404(Product, id=obj.book_product.id)
        if product.public: 
            return super().get(request, *args, **kwargs)
        return redirect('ebooks:book-detail', book_slug=obj.slug)
        

class BookDetailView(EbookView, DetailView):
    """ Returns the digital content of a product. """
    
    model = Book
    slug_url_kwarg = 'book_slug'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.published().product()

    def get_template_names(self):
        return ['ebooks/book_detail_%s.html' % self.object.template]


class PaperEbookView(BookDetailView):
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
        current_lan = get_language()
        paper_filename = get_paper_filename(paper_id=self.object.id, paper_lan=current_lan)
        paper_soup = parse_paper_soup(paper_filename)
        # context['paper_title'] = paper_soup.select_one('.ace-line').extract().get_text()
        context['paper_title'] = self.object.title
        context['paper_toc'] = make_paper_toc(paper_soup)
        context['book_paper'] = paper_filename
        return context


class PublicPaperEbookView(PublicEbookMixin, PaperEbookView):
    """
        Renders the ebook regardless of the user or their collection.
    """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.object.book_product.related_products.all()
        return context


class PrivatePaperEbookView(LoginRequiredMixin, UserHasProductMixin, PaperEbookView):
    """
        Renders the ebook if and only if the user is authenticated 
        and has the product in their collection.
    """
    pass