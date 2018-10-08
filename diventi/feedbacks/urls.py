from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import SurveyListView, SurveyDetailView

app_name = 'feedbacks'

urlpatterns = [
    url(r'^$', SurveyListView.as_view(), name='list'),
    url(_(r'^(?P<slug>[-\w]+)/$'), SurveyDetailView.as_view(), name='detail'),
]