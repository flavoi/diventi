from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import file_challenge

app_name = 'brave'

urlpatterns = [
    path(_('brave-rewards-verification.txt/'), file_challenge),
]