from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import HomePageView, charge

app_name = 'payments'

urlpatterns = [
    path(_(''), HomePageView.as_view(), name='home'),
    path(_('charge/<slug:product_slug>/'), charge, name='charge'),
]