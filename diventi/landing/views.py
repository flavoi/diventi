from itertools import chain

from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Presentation, Feedback
from .forms import FeedbackCreationForm
from diventi.accounts.models import DiventiUser
from diventi.accounts.forms import DiventiUserInitForm
from diventi.products.models import Product
from diventi.blog.models import Article


def landing(request):
    """ 
        Renders the landing page with Diventi's main features and
        team members. 
    """
    presentation = Presentation.objects.active()    
    featured_product = Product.objects.featured()
    if request.method == 'POST':
        registration_form = DiventiUserInitForm(request.POST)
        if registration_form.is_valid():
            # Save the user inputs and pass them to the sign up page
            request.session['initial_email'] = registration_form['email'].value()
            request.session['initial_first_name'] = registration_form['first_name'].value()
            return redirect('accounts:signup')
    else:
        registration_form = DiventiUserInitForm()

    context = {   
        'presentation': presentation,
        'registration_form': registration_form,
        'featured_product': featured_product,
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
    """ Renders an instance of the landing page.. """

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


class FeedbackCreationView(LoginRequiredMixin, CreateView):
    """ Insert a new feedback linked to the user """

    form_class = FeedbackCreationForm
    model = Feedback
    template_name = 'landing/feedback.html'
    success_msg = _('You feedback has been sent!')

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(FeedbackCreationView, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:            
            return next_url
        else:
            super().get_success_url()

