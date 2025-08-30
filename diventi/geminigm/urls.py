from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    send_message,
    list_messages,
)

app_name = 'geminigm'

urlpatterns = [
    path(_('send'), send_message, name='send_message'),
    path('', list_messages, name='list_messages'),
]