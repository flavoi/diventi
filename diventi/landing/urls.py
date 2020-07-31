from django.conf.urls import url
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    landing, 
    PresentationSearchView, 
    landing_survey,
    DashboardView,
    QuickTemplateView,
)

app_name = 'landing'

urlpatterns = [
    path('', QuickTemplateView.as_view(), name='home'),
]

urlpatterns += [
    path('legacy/', landing, name='home_legacy'),
    path(_('search/'), PresentationSearchView.as_view(), name='search'),
    path(_('survey/'), landing_survey, name='survey'),
    path(_('analytics/'), DashboardView.as_view(), name='analytics'),
]