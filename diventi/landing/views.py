from itertools import chain

from django.shortcuts import render, redirect, resolve_url
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseNotFound

from diventi.accounts.models import DiventiUser
from diventi.accounts.forms import DiventiUserInitForm
from diventi.products.models import Product
from diventi.blog.models import Article
from diventi.feedbacks.models import Survey, Answer
from diventi.core.views import StaffRequiredMixin

from .models import (
    Section,
    AboutArticle,
    PolicyArticle,
)


class LandingSearchView(ListView):
    """ Search for every content in the project. """

    template_name = "landing/search_results_quick.html"
    context_object_name = 'results'
    model = Section

    def get_queryset(self):
        results = super(LandingSearchView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            articles = Article.search(self, query)
            products = Product.search(self, query)
            users = DiventiUser.search(self, query)
            results = list(chain(products, articles, users))
        else:
            results = None
        return results

    def get_context_data(self, **kwargs):
        context = super(LandingSearchView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        return context


class DashboardView(StaffRequiredMixin, ListView):
    """ Report relevant piece of contents of any supported app. """

    template_name = "landing/analytics_quick.html"
    context_object_name = 'results'
    model = Section

    def get_queryset(self):
        results = super(DashboardView, self).get_queryset()
        articles = Article.reporting(self)
        products = Product.reporting(self)
        users = DiventiUser.reporting(self)
        results = list(chain(users,articles, products, ))
        return results

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        featured_section = Section.objects.featured()
        context['featured_section'] = featured_section
        return context


def get_landing_context(request):
    sections = Section.objects.not_featured()
    featured_section = Section.objects.featured()
    latest_articles = Article.objects.history()[:5]
    if featured_section:
        pass
    elif sections.exists():
        featured_section = sections.first()
        sections = sections.exclude(id=featured_section.id)
    else:
        return HttpResponseNotFound(_('This page is not available yet.'))
    context = {   
        'sections': sections,
        'featured_section': featured_section,
        'latest_articles': latest_articles, 
    }
    return context


class LandingTemplateView(TemplateView):
    """ Renders the landing page with all necessary context. """

    template_name = "landing/landing_quick.html"

    def get_context_data(self, **kwargs):
        context = super(LandingTemplateView, self).get_context_data(**kwargs)
        landing_context = get_landing_context(self.request)
        context = {**context, **landing_context} # Merge the two dictionaries
        return context


class AboutArticleDetailView(DetailView):
    """ Renders the 'about us' article and the content related to it. """
    
    model = AboutArticle
    template_name  = "landing/about_article_quick.html"


class PolicyArticleDetailView(DetailView):
    """ Renders the policy article and the content related to it. """
    
    model = PolicyArticle
    template_name  = "landing/about_article_quick.html"






