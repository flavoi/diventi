from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import BookDetailView, ChapterDetailView, SectionSearchView, SectionDetailView, ChapterAutocomplete

app_name = 'ebooks'

urlpatterns = [
    path(_('book/<slug:book_slug>/'), BookDetailView.as_view(), name='book-detail'),
    path(_('book/<slug:book_slug>/chapter/<slug:chapter_slug>/'), ChapterDetailView.as_view(), name='chapter-detail'),
    path(_('book/<slug:book_slug>/chapter/<slug:chapter_slug>/<slug:section_slug>-<int:section_pk>/'), SectionDetailView.as_view(), name='section-detail'),
    path(_('book/<slug:book_slug>/search/'), SectionSearchView.as_view(), name='section-search'),
    path(_('chapter-autocomplete/'), ChapterAutocomplete.as_view(), name='chapter-autocomplete',),
]