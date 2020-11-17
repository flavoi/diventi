from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.conf import settings

from dal import autocomplete

from diventi.core.views import StaffRequiredMixin
from diventi.core.utils import (
    get_dropbox_paper_soup, 
    adjust_paper_visual_styles,
    render_paper_images_by_direct_url,
    remove_dropbox_placeholders,
)
from diventi.products.models import Product
from diventi.tooltips.models import (
    TooltipGroup,
    Tooltip,
)

from .models import (
    Book, 
    Chapter, 
    Section, 
    UniversalSection,
)

from .utils import (    
    make_paper_toc,
    render_diventi_snippets,
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
        chapters = Chapter.objects.filter(chapter_book__slug=book_slug)
        chapters = chapters.order_by('order_index', 'part').bookmark_sections()
        context['chapters'] = chapters
        tooltip_group = TooltipGroup.objects.filter(books=book).first()
        if tooltip_group:
            tooltips = tooltip_group.tooltips.all().prefetch()
            context['tooltips'] = tooltips
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_chapter = self.object.chapters.order_by('order_index').first()
        context['next_chapter'] = first_chapter
        return context

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
        adjust_paper_visual_styles(paper_soup)
        render_paper_images_by_direct_url(paper_soup)
        remove_dropbox_placeholders(paper_soup)
        output_soup = paper_soup.select_one('.ace-editor')
        context['paper_content'] = str(output_soup)
        f = open("./test_soup.html", "a")
        f.write(mark_safe(str(output_soup)))
        f.close()
        return context


class ChapterDetailView(LoginRequiredMixin, UserHasProductMixin,
                        EbookView, DetailView):
    """ Returns the chapter of a book. """
    
    model = Chapter
    template_name = "ebooks/chapter_detail.html"
    slug_url_kwarg = 'chapter_slug'
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        book_slug = self.kwargs.get('book_slug')
        book = get_object_or_404(Book, slug=book_slug) 
        queryset = queryset.filter(chapter_book=book)
        return queryset.published().sections()

    def get_template_names(self):
        return ['ebooks/chapter_detail_%s.html' % self.object.chapter_book.template]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapters = context['chapters']
        next_chapter = chapters.filter(order_index__gt=self.object.order_index)
        next_chapter = next_chapter.order_by('order_index')
        next_chapter = next_chapter.first()
        context['next_chapter'] = next_chapter
        previous_chapter = chapters.filter(order_index__lt=self.object.order_index)
        previous_chapter = previous_chapter.order_by('-order_index')
        previous_chapter = previous_chapter.first()
        context['previous_chapter'] = previous_chapter
        table_of_contents = Section.objects.filter(chapter=self.object).bookmarks()
        context['table_of_contents'] = table_of_contents
        return context


class SectionSearchView(LoginRequiredMixin, UserHasProductMixin,
                        EbookView, ListView):
    """
        Returns a list of sections that matches the searched phrase.
    """

    model = Section
    context_object_name = 'results'


    def get_queryset(self, **kwargs):
        results = super().get_queryset(**kwargs)
        query = self.request.GET.get('q')
        book_slug = self.kwargs.get('book_slug')
        if query:
            sections = Section.search(self, query, book_slug)
            results = list(chain(sections,))
        else:
            results = None
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        return context

    def get_template_names(self):
        book_slug = self.kwargs.get('book_slug', None)
        book = get_object_or_404(Book, slug=book_slug)
        return ['ebooks/search_results_%s.html' % book.template]


class SectionDetailView(LoginRequiredMixin, UserHasProductMixin,
                        EbookView, DetailView):
    """ Returns the chapter of a book. """
    
    model = Section
    template_name = "ebooks/section_detail.html"
    pk_url_kwarg = 'section_pk'
    
    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        chapter = Chapter.objects.filter(id=obj.chapter.id)
        chapter = chapter.published()
        try:
            chapter = chapter.get()
        except chapter.model.DoesNotExist:
            raise Http404(_("This book hasn't been published yet."))
        section = Section.objects.usection().get(id=obj.id) # Select related objects
        return section

    def get_template_names(self):
        book_slug = self.kwargs.get('book_slug', None)
        book = get_object_or_404(Book, slug=book_slug)
        return ['ebooks/section_detail_%s.html' % book.template]


class ChapterAutocomplete(autocomplete.Select2QuerySetView, StaffRequiredMixin):
    """ Returns filtered chapters to facilitate user form fill. """
  
    def get_queryset(self):
        qs = Chapter.objects.all().book()
        book = self.forwarded.get('book', None)
        if book:
            qs = qs.filter(chapter_book=book)
        if self.q:
            qs = qs.filter(title__icontains=self.q)
        return qs


class SectionAutocompleteFromProduct(autocomplete.Select2QuerySetView, StaffRequiredMixin):
    """ Returns filtered sections to facilitate user form fill. """

    def get_queryset(self):
        qs = Section.objects.all().usection()
        product = self.forwarded.get('product', None)
        if product:
            book = Book.objects.filter(book_product=product)
            qs = qs.filter(chapter__chapter_book=book[0])
        if self.q:
            qs = qs.filter(title__icontains=self.q)
        return qs