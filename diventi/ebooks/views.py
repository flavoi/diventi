from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Chapter


class ChapterDetailView(DetailView):
    """ Returns the digital content of a product. """
    
    model = Chapter
    template_name = "ebooks/chapter_detail.html"
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.sections() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = Chapter.objects.all().order_by('order_index')
        return context