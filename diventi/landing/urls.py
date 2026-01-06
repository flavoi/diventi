from django.conf.urls import url
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    LandingSearchView,
    DashboardView,
    LandingTemplateView,
    AboutArticleDetailView,
    LandingPageDetailView,
)

app_name = 'landing'

urlpatterns = [
    path('', LandingTemplateView.as_view(), name='home'),
    path(_('search/'), LandingSearchView.as_view(), name='search'),
    path(_('analytics/'), DashboardView.as_view(), name='analytics'),
    path(_('about/<slug:slug>/'), AboutArticleDetailView.as_view(), name='about'),
    path(_('page/<slug:slug>/'), LandingPageDetailView.as_view(), name='page_detail'),
]