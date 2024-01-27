from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    PrivatePaperEbookView,
    PublicPaperEbookView,
    PrivatePdfEbookView,
    PublicPdfEbookView,
)

app_name = 'ebooks'

urlpatterns = [    
    path(_('paper/<slug:book_slug>/'), PrivatePaperEbookView.as_view(), name='book-detail'),    
    path(_('paper/<slug:book_slug>/language/<language_code>/'), PrivatePaperEbookView.as_view(), name='book-detail-customlan'),
    path(_('paper/<slug:book_slug>/public/'), PublicPaperEbookView.as_view(), name='book-detail-public'),
    path(_('pdf/<slug:book_slug>/'), PrivatePdfEbookView.as_view(), name='pdf-detail'),
    path(_('pdf/<slug:book_slug>/public/'), PublicPdfEbookView.as_view(), name='pdf-detail-public'),
]