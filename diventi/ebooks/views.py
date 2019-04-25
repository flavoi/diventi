from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Section


class SectionDetailView(DetailView):
    """ Returns the digital content of a product. """
    
    model = Section
    template_name = "ebooks/section_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all().order_by('order_index')
        return context