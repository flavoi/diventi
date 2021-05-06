from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)
from django.http import Http404
from django.conf import settings

from diventi.products.models import Product

from .models import Book

from .utils import (
    get_dropbox_paper_soup, 
    render_paper_tables,
    render_paper_images_by_direct_url,
    render_paper_code_blocks,
    remove_dropbox_placeholders,
    render_paper_hr,
    render_paper_headings,
    render_diventi_snippets,
    render_paper_images,
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


class BookDetailView(LoginRequiredMixin, UserHasProductMixin, 
                     EbookView, DetailView):
    """ Returns the digital content of a product. """
    
    model = Book
    slug_url_kwarg = 'book_slug'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.published().product()

    def get_template_names(self):
        return ['ebooks/book_detail_%s.html' % self.object.template]


from django.utils.safestring import mark_safe
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
        paper_id = self.object.paper_id        
        paper_soup = get_dropbox_paper_soup(paper_id)
        diventi_universale_soup = get_dropbox_paper_soup(settings.DIVENTI_UNIVERSALE_PAPER_ID)
        context['paper_title'] = paper_soup.select_one('.ace-line').extract().get_text()
        context['paper_toc'] = make_paper_toc(paper_soup)
        render_diventi_snippets(paper_soup, diventi_universale_soup)
        render_paper_tables(paper_soup)
        render_paper_images(paper_soup)
        render_paper_code_blocks(paper_soup)
        #remove_dropbox_placeholders(paper_soup)
        render_paper_hr(paper_soup)
        render_paper_headings(paper_soup)
        context['paper_content'] = str(paper_soup)
        if settings.PRINT_HTML_EBOOK:
            print('Storicizzo paper in formato html in {}.'.format(settings.PROJ_ROOT))
            with open(settings.PROJ_ROOT / 'paper_content.html', 'w') as file:
                file.write(str(paper_soup))

        return context