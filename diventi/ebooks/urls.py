from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import SectionListView

app_name = 'ebooks'

urlpatterns = [
	path(_('demo'), SectionListView.as_view(), name='sections'),
]