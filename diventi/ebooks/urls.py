from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    PrivatePaperEbookView,
    PublicPaperEbookView,
)

app_name = 'ebooks'

urlpatterns = [
    path(_('paper/public/<slug:book_slug>/'), PublicPaperEbookView.as_view(), name='book-detail-public'),
    path(_('paper/<slug:book_slug>/'), PrivatePaperEbookView.as_view(), name='book-detail'),
    path(_('paper/<slug:book_slug>/language/<language_code>/'), PrivatePaperEbookView.as_view(), name='book-detail-customlan'),
]