from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import PaperDetailView

app_name = 'homebrew'

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', PaperDetailView.as_view(), name='detail'),
]