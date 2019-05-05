from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from diventi.products.models import Product
from .models import Book, Chapter


class UserHasProductMixin(UserPassesTestMixin):
    """ 
        This view checks if the user has bought the product
        related to the requested book. 
        It assumes to have the slug of the book object available
        in book_slug get parameter.
    """

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
        chapters = Chapter.objects.filter(chapter_book__slug=book_slug)
        chapters = chapters.order_by('order_index')
        context['chapters'] = chapters
        return context


class BookDetailView(LoginRequiredMixin,
                     UserHasProductMixin,
                     EbookView,
                     DetailView):
    """ Returns the digital content of a product. """
    
    model = Book
    template_name = "ebooks/book_detail.html"
    slug_url_kwarg = 'book_slug'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.product()


class ChapterDetailView(LoginRequiredMixin,
                        UserHasProductMixin,
                        EbookView, 
                        DetailView):
    """ Returns the chapter of a book. """
    
    model = Chapter
    template_name = "ebooks/chapter_detail.html"
    slug_url_kwarg = 'chapter_slug'
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.sections()