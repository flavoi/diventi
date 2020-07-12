from itertools import chain

from django.shortcuts import render, redirect, resolve_url
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponse

from diventi.accounts.models import DiventiUser
from diventi.accounts.forms import DiventiUserInitForm
from diventi.products.models import Product
from diventi.blog.models import Article
from diventi.feedbacks.models import Survey, Answer
from diventi.core.views import StaffRequiredMixin

from .models import Section

def landing_survey(request):
    """
        Redirect te user to the survey included in the current section.
    """
    if request.method == 'POST':
        featured_survey_form = FeaturedSurveyInitForm(request.POST)
        if featured_survey_form.is_valid():
            survey = featured_survey_form.cleaned_data['survey']
            author_name = featured_survey_form.cleaned_data['author_name']
            return redirect(reverse('feedbacks:questions-author', kwargs={'slug': survey.slug, 'author_name': author_name}))
        else:
            messages.error(request, _('We encountered an error while redirecting to your survey.'))
    return redirect('landing:home')


def landing(request):
    """ 
        Renders the landing page with Diventi main features and
        team members. 
    """
    sections = Section.objects.not_featured()
    featured_section = Section.objects.featured()
    if featured_section:
        pass
    elif sections.exists():
        featured_section = sections.first()
        sections = sections.exclude(id=featured_section.id)
    else:
        return HttpResponse(_('This page is not available yet.'))

    if request.method == 'POST':
        registration_form = DiventiUserInitForm(request.POST)
        if registration_form.is_valid():
            # Save the user inputs and pass them to the sign up page
            request.session['initial_email'] = registration_form['email'].value()
            request.session['initial_first_name'] = registration_form['first_name'].value()            
        else:
            messages.info(request, _('Please double check your email.'))
            request.session.flush()
        return redirect('accounts:signup')
    else:
        registration_form = DiventiUserInitForm()

    context = {   
        'registration_form': registration_form,
        'sections': sections,
        'featured_section': featured_section,
    }

    return render(request, 'landing/landing.html', context)


class PresentationSearchView(ListView):
    """ Search for every content in the project. """

    template_name = "landing/search_results.html"
    context_object_name = 'results'
    model = Section

    def get_queryset(self):
        results = super(PresentationSearchView, self).get_queryset()
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
        context = super(PresentationSearchView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        return context


class DashboardView(StaffRequiredMixin, ListView):
    """ Report relevant piece of contents of any supported app. """

    template_name = "landing/analytics.html"
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


class QuickTemplateView(TemplateView):
    """ Initial implementation of quick visual style. """

    template_name = "landing/landing_quick.html"



