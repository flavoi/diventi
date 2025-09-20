from itertools import chain

from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic import (
    ListView,
    TemplateView,
    RedirectView
)

from django.views.generic.edit import CreateView
from django.utils.translation import (
    ugettext_lazy as _,
    get_language,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseNotFound

from hitcount.views import HitCountDetailView

from diventi.accounts.forms import DiventiUserInitForm

from diventi.accounts.models import DiventiUser
from diventi.products.models import Product
from diventi.blog.models import Article
from diventi.ebooks.models import Book
from diventi.feedbacks.models import Survey
from diventi.packages.models import Package

from diventi.core.views import StaffRequiredMixin

from .models import (
    Section,
    AboutArticle,
)

from diventi.ebooks.utils import (
    get_paper_filename,
    parse_paper_soup,
    make_paper_toc,
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
            packages = Package.search(self, query)
            results = list(chain(products, articles, users, packages))
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
        results = []
        results.append((_('users'), DiventiUser.reporting(self)))
        results.append((_('packages'), Package.reporting(self)))
        results.append((_('popular articles'), Article.reporting_popular(self)))
        results.append((_('latest articles'), Article.reporting_latest(self)))
        results.append((_('about articles'), AboutArticle.reporting(self)))
        results.append((_('private products'), Product.reporting_private(self)))
        results.append((_('popular public products'), Product.reporting_public_popular(self)))
        results.append((_('latest public products'), Product.reporting_public_recent(self)))
        return results

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        featured_section = Section.objects.featured()
        context['featured_section'] = featured_section
        return context


def get_landing_context(request):
    sections = Section.objects.not_featured()

    featured_product = Product.objects.pinned_list().featured()
    pinned_product = Product.objects.pinned()
    latest_public_product = Product.objects.latest_public()
    latest_article = Article.objects.hottest()
    pinned_survey = Survey.objects.pinned()
    featured_package = Package.objects.pinned_list().featured()
    pinned_package = Package.objects.pinned()

    featured_section = Section.objects.featured()
    if featured_section:
        pass
    elif sections.exists():
        featured_section = sections.first()
        sections = sections.exclude(id=featured_section.id)
    else:
        return HttpResponseNotFound(_('This page is not available yet.'))

    sections = Section.objects.not_featured()

    context = {
        'featured_product': featured_product,
        'pinned_product': pinned_product,
        'featured_section': featured_section,
        'sections': sections,
        'latest_article': latest_article,
        'latest_public_product': latest_public_product,
        'pinned_survey': pinned_survey,
        'featured_package': featured_package,
        'pinned_package': pinned_package,
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


class AboutArticleDetailView(HitCountDetailView):
    """ Renders the 'about us' article and the content related to it. """
    
    model = AboutArticle
    count_hit = True
    template_name  = "landing/about_article_quick.html"




