from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

from diventi.products.models import Product
from .models import Book, Chapter, Section


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
        test = product.user_has_already_bought(self.request.user) or product.user_has_authored(self.request.user)
        return test


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
        chapters = chapters.order_by('order_index').bookmark_sections()
        context['chapters'] = chapters
        return context


class BookDetailView(LoginRequiredMixin, UserHasProductMixin,
                     EbookView, DetailView):
    """ Returns the digital content of a product. """
    
    model = Book
    #template_name = "ebooks/book_detail.html"
    slug_url_kwarg = 'book_slug'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.published().product()

    def get_template_names(self):
        return ['ebooks/book_detail_%s.html' % self.object.template]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_chapter = self.object.chapters.first()
        context['next_chapter'] = first_chapter
        return context


class ChapterDetailView(LoginRequiredMixin, UserHasProductMixin,
                        EbookView, DetailView):
    """ Returns the chapter of a book. """
    
    model = Chapter
    template_name = "ebooks/chapter_detail.html"
    slug_url_kwarg = 'chapter_slug'
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
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
        chapter = Chapter.objects.filter(slug=obj.chapter.slug)
        chapter = chapter.published()
        try:
            chapter = chapter.get()
        except chapter.model.DoesNotExist:
            raise Http404(_("This book hasn't been published yet."))
        return obj