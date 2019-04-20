from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import landing, PresentationSearchView, landing_survey

app_name = 'landing'

urlpatterns = [
    url(r'^$', landing, name='home'),
    url(_(r'^search/$'), PresentationSearchView.as_view(), name='search'),
    url(_(r'^survey/$'), landing_survey, name='survey'),
]