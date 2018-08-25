from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tex.views import render_to_pdf

from .models import Paper, Section, Watermark
from .utils import brew_to_pdf


class PaperDetailView(LoginRequiredMixin, DetailView):

    model = Paper
    context_object_name = 'paper'
    template_name = 'paper.tex'

    def get_context_data(self, *args, **kwargs):
        context = super(PaperDetailView, self).get_context_data(*args, **kwargs)
        sections = Section.objects.filter(paper=self.object).order_by('order_id')
        sections = sections.select_related('table')
        sections = sections.prefetch_related('table__rows')
        context['sections'] = sections
        context['watermarks'] = Watermark.objects.filter(paper=self.object).order_by('pages')
        return context

    def get(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return brew_to_pdf(self.template_name, context, filename='test.pdf')