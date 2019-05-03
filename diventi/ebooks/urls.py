from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import BookDetailView, ChapterDetailView

app_name = 'ebooks'

urlpatterns = [
	path(_('<slug:book_slug>/'), BookDetailView.as_view(), name='book-detail'),
	path(_('<slug:book_slug>/chapter/<slug:chapter_slug>/'), ChapterDetailView.as_view(), name='chapter-detail'),
]