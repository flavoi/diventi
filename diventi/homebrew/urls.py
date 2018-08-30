from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import HomebrewHome, PaperDetailView, PaperDetailTexView

app_name = 'homebrew'

urlpatterns = [
    url(r'^$', HomebrewHome.as_view(), name='home'),
    url(r'^(?P<slug>[-\w]+)/$', PaperDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/tex/$', PaperDetailTexView.as_view(), name='detail_tex'),
]