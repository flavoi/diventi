from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ingest_document_view,
    chatbot_view,
)

app_name = 'geminigm'

urlpatterns = [
    path(_('ingest/'), ingest_document_view, name='ingest_document'),
    path('', chatbot_view, name='chatbot'),
]