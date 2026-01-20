from itertools import chain

from django.conf import settings
from django.views.generic.detail import DetailView
from django.views.generic import (
    ListView,
    TemplateView,
)
from django.views import View
from django.utils.translation import (
    ugettext_lazy as _,
    get_language,
)
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string

from hitcount.views import HitCountDetailView

from diventi.accounts.models import DiventiUser
from diventi.products.models import Product
from diventi.products.utils import get_product_context
from diventi.blog.models import Article
from diventi.feedbacks.models import Survey
from diventi.packages.models import Package
from diventi.core.views import StaffRequiredMixin

from .models import (
    Section,
    AboutArticle,
    LandingPage,
)
from .utils import get_landing_context


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

    template_name = "landing/analytics2_quick.html"
    context_object_name = 'results'
    model = Section

    def get_queryset(self):
        results = []
        """
        results.append((_('users'), DiventiUser.reporting(self)))
        results.append((_('packages'), Package.reporting(self)))
        results.append((_('popular articles'), Article.reporting_popular(self)))
        results.append((_('latest articles'), Article.reporting_latest(self)))
        results.append((_('about articles'), AboutArticle.reporting(self)))
        results.append((_('private products'), Product.reporting_private(self)))
        results.append((_('popular public products'), Product.reporting_public_popular(self)))
        results.append((_('latest public products'), Product.reporting_public_recent(self)))
        """
        results.append((_('users'), 'users'))
        results.append((_('packages'), 'packages'))
        results.append((_('popular articles'), 'articles_popular'))
        results.append((_('latest articles'), 'articles_latest'))
        results.append((_('about articles'), 'about_articles'))
        results.append((_('private products'), 'products_private'))
        results.append((_('popular public products'), 'products_public_popular'))
        results.append((_('latest public products'), 'products_public_latest'))
        return results

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        featured_section = Section.objects.featured()
        context['featured_section'] = featured_section
        return context


class AnalyticsCardView(StaffRequiredMixin, View):
    def get(self, request, card_type):
        results = []        

        # Eseguiamo solo la query richiesta
        if card_type == 'users':
            data = DiventiUser.reporting(self)
            title = _('users')
        elif card_type == 'packages':
            data = Package.reporting(self)
            title = _('packages')
        elif card_type == 'articles_popular':
            data = Article.reporting_popular(self)
            title = _('popular articles')
        elif card_type == 'articles_latest':
            data = Article.reporting_latest(self)
            title = _('latest articles')
        elif card_type == 'about_articles':
            data = AboutArticle.reporting(self)
            title = _('about articles')
        elif card_type == 'products_private':
            data = Product.reporting_private(self)
            title = _('private products')
        elif card_type == 'products_public_popular':
            data = Product.reporting_public_popular(self)
            title = _('popular public products')
        elif card_type == 'products_public_latest':
            data = Product.reporting_public_recent(self)
            title = _('latest public products')
        else:
            return JsonResponse({'error': 'Invalid card type'}, status=400)


        # Rendiamo solo il pezzetto di HTML relativo alla card
        # Creiamo un template parziale '_card_partial.html' che contiene 
        # solo la logica interna del tuo attule loop
        html = render_to_string('landing/partials/_analytics_card.html', {
            'title': title,
            'data': data, 
        }, request=request)

        return JsonResponse({'html': html})


class LandingTemplateView(TemplateView):
    """ Renders the landing page with all necessary context. """

    template_name = "landing/landing_quick.html"

    def get_context_data(self, **kwargs):
        context = super(LandingTemplateView, self).get_context_data(**kwargs)
        page = LandingPage.objects.featured()
        landing_context = get_landing_context(self.request, page=page)
        context = {**context, **landing_context}
        self.template_name = page.theme
        return context


class AboutArticleDetailView(HitCountDetailView):
    """ Renders the 'about us' article and the content related to it. """
    
    model = AboutArticle
    count_hit = True
    template_name  = "landing/about_article_quick.html"


class LandingPageDetailView(StaffRequiredMixin, DetailView):
    """ Renders a landing page """

    template_name = "landing/landing_quick.html"
    model = LandingPage
    context_object_name = 'page'

    def get_queryset(self):
        qs = super(LandingPageDetailView, self).get_queryset()
        return qs.published()

    def get_context_data(self, **kwargs):
        context = super(LandingPageDetailView, self).get_context_data(**kwargs)     
        landing_context = get_landing_context(self.request, self.object)
        self.template_name = self.object.theme
        context = {**context, **landing_context}     
        return context
