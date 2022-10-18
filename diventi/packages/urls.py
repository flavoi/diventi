from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    PackageDetailView,
)

app_name = 'packages'

urlpatterns = [
    path(_('<slug:slug>/'), PackageDetailView.as_view(), name='detail'),
]