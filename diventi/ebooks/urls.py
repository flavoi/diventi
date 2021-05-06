from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    PaperEbookView,
)

app_name = 'ebooks'

urlpatterns = [
    path(_('paper/<slug:book_slug>/'), PaperEbookView.as_view(), name='book-detail'),
]