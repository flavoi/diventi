from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import SectionDetailView

app_name = 'ebooks'

urlpatterns = [
	path('<slug:slug>/', SectionDetailView.as_view(), name='detail'),
]