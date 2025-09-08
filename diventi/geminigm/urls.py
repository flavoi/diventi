from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ingest_document_view,
    chatbot_view,
    send_message_ajax,
)

app_name = 'geminigm'

urlpatterns = [
    path(_('ingest/'), ingest_document_view, name='ingest_document'),
    path('', chatbot_view, name='chatbot'),
    path('send_message_ajax/', send_message_ajax, name='send_message_ajax'),
]