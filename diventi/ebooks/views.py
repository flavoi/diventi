from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Section


class SectionListView(TemplateView):
    """ Returns the digital content of a product. """

    template_name = "ebooks/section_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        return context