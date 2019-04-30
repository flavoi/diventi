from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import ChapterDetailView

app_name = 'ebooks'

urlpatterns = [
	path(_('<slug:chapter_book>/chapter/<slug:slug>/'), ChapterDetailView.as_view(), name='chapter-detail'),
]