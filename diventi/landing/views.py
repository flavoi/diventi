from itertools import chain

from django.shortcuts import render, redirect, resolve_url
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Presentation, Section
from diventi.accounts.models import DiventiUser
from diventi.accounts.forms import DiventiUserInitForm
from diventi.products.models import Product
from diventi.blog.models import Article
from diventi.feedbacks.forms import FeaturedSurveyInitForm
from diventi.feedbacks.models import Survey, Answer


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
    authors = DiventiUser.objects.authors()
    products = Product.objects.published()
    featured_section = Section.objects.featured()
    sections = Section.objects.not_featured()
    sections = sections.prefetch_related('users')
    sections = sections.prefetch_related('products')
    sections = sections.order_by('order_index')

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
        if featured_section.section_survey:
            featured_survey_data = {
                'survey': featured_section.section_survey,
            }
            featured_survey_form = FeaturedSurveyInitForm(initial = featured_survey_data)
        else:
            featured_survey_form = None

    context = {   
        'registration_form': registration_form,
        'featured_survey_form': featured_survey_form,
        'products': products,
        'authors': authors,
        'sections': sections,
        'featured_section': featured_section,
    }

    # This session variable enables and error message in the login modal.
    if request.session.get('show_login_form', None):
        context['show_login_form'] = 1
        del request.session['show_login_form']
    if request.session.get('fail_login_msg', None):
        context['fail_login_msg'] = request.session.get('fail_login_msg')
        del request.session['fail_login_msg']

    return render(request, 'landing/landing.html', context)


class PresentationDetailView(DetailView):
    """ Renders an instance of the landing page. """

    model = Presentation
    context_object_name = 'presentation'
    template_name = 'landing/landing.html'

    def get_context_data(self, **kwargs):
        context = super(PresentationDetailView, self).get_context_data(**kwargs)
        context['staff'] = DiventiUser.objects.members()
        context['registration_form'] = DiventiUserInitForm()
        context['featured_product'] = Product.objects.featured()
        return context


class PresentationSearchView(ListView):
    """ Search for every content in the project. """

    model = Presentation
    template_name = "landing/search_results.html"
    context_object_name = 'results'

    def get_queryset(self):
        results = super(PresentationSearchView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            articles = Article.search(self, query)
            products = Product.search(self, query)
            users = DiventiUser.search(self, query)
            results = chain(articles, products, users)
        else:
            results = None
        return results

    def get_context_data(self, **kwargs):
        context = super(PresentationSearchView, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        return context
