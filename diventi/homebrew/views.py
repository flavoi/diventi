from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from django_tex.views import render_to_pdf

from diventi.core.views import StaffRequiredMixin

from .models import Paper, Section, Watermark
from .utils import render_to_pdf, render_to_tex


class PaperDetailView(StaffRequiredMixin, DetailView):

    model = Paper
    context_object_name = 'paper'
    

    def get_context_data(self, *args, **kwargs):
        context = super(PaperDetailView, self).get_context_data(*args, **kwargs)
        sections = Section.objects.filter(paper=self.object).order_by('order_id')
        sections = sections.tables()
        sections = sections.lists()
        sections = sections.characters()
        context['contents'] = _('contents')
        babel = self.request.LANGUAGE_CODE
        if babel == 'it':
            context['babel'] = 'italian'
        else:
            context['babel'] = 'english'
        context['sections'] = sections
        context['watermarks'] = Watermark.objects.filter(paper=self.object).order_by('pages')
        return context

    def get(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render_to_pdf(self.get_template_name(), context, filename='test.pdf')

    def get_template_name(self):
        """
        Return the template that has been configured for this paper. 
        """
        if self.object.template is None:
            raise ImproperlyConfigured(
                _("This paper requires a template.'"))
        else:
            return self.object.template


class PaperDetailTexView(PaperDetailView):

    def get(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render_to_tex(request, self.template_name, context)
