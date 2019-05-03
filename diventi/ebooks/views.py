from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views import View

from .models import Book, Chapter


class EbookView(View):
    """ Generic view that manages context data for ebooks. """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_slug = self.kwargs.get('book_slug', None)
        chapters = Chapter.objects.filter(chapter_book__slug=book_slug)
        chapters = chapters.order_by('order_index')
        context['chapters'] = chapters
        return context


class BookDetailView(EbookView, DetailView):
    """ Returns the digital content of a product. """
    
    model = Book
    template_name = "ebooks/book_detail.html"
    slug_url_kwarg = 'book_slug'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.product()


class ChapterDetailView(EbookView, DetailView):
    """ Returns the chapter of a book. """
    
    model = Chapter
    template_name = "ebooks/chapter_detail.html"
    slug_url_kwarg = 'chapter_slug'
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.sections()