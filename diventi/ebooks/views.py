from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Chapter


class ChapterDetailView(DetailView):
    """ Returns the digital content of a product. """
    
    model = Chapter
    template_name = "ebooks/chapter_detail.html"
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        book_slug = self.kwargs.get('chapter_book', None)
        if book_slug is not None:
            queryset = queryset.filter(chapter_book__slug=book_slug)
            queryset = queryset.sections()
            return queryset
        else: 
            return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = Chapter.objects.all().order_by('order_index')
        return context
        