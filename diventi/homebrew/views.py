from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .models import Brew
from .utils import brew_to_pdf


class BrewView(TemplateView):
    """ Displays the about page. """
    template_name = 'homebrew/brew.html'


def testview(request):
    template_name = 'test.tex'
    context = {}
    return brew_to_pdf(template_name, context, filename='test.pdf')


class BrewDetailView(DetailView):

    model = Brew
    context_object_name = 'brew'