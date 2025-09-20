from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ingest_document_view,
    chatbot_view,
    send_message_ajax,
    get_char_sheet_ajax,
    get_adventure_summary_ajax,
    PrivateGemmaView,
    PublicGemmaView,
)

app_name = 'geminigm'

urlpatterns = [
    path(_('ingest/'), ingest_document_view, name='ingest_document'),
    path('gemma/<slug:gemma_slug>/', PrivateGemmaView.as_view(), name='gemma_private'),
    path(_('gemma/<slug:gemma_slug>/public/'), PublicGemmaView.as_view(), name='gemma_public'), 
    path('send_message_ajax/<slug:gemma_slug>/', send_message_ajax, name='send_message_ajax'),    
    path('get_adventure_summary_ajax/<slug:gemma_slug>/', get_adventure_summary_ajax, name='get_adventure_summary_ajax'),
    path('get_char_sheet_ajax/<slug:gemma_slug>/', get_char_sheet_ajax, name='get_char_sheet_ajax'),
]