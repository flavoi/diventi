from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import BrewView, testview, BrewDetailView

app_name = 'homebrew'

urlpatterns = [
    url(r'^$', BrewView.as_view(), name='brew'),
    url(r'^test/$', testview, name='test'),
    url(_(r'^(?P<slug>[-\w]+)/$'), BrewDetailView.as_view(), name='detail'),
]