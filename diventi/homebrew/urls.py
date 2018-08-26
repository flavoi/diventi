from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import HomebrewHome, PaperDetailView

app_name = 'homebrew'

urlpatterns = [
    url(r'^$', HomebrewHome.as_view(), name='home'),
    url(r'^(?P<slug>[-\w]+)/$', PaperDetailView.as_view(), name='detail'),
]