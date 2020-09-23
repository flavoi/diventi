from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    BookDetailView,
    PaperEbookView,
    ChapterDetailView,
    SectionSearchView,
    SectionDetailView,
    ChapterAutocomplete,
    SectionAutocompleteFromProduct,
)

app_name = 'ebooks'

urlpatterns = [
    path(_('book/<slug:book_slug>/'), BookDetailView.as_view(), name='book-detail-legacy'),
    path(_('paper/<slug:book_slug>/'), PaperEbookView.as_view(), name='book-detail'),
    path(_('book/<slug:book_slug>/chapter/<slug:chapter_slug>/'), ChapterDetailView.as_view(), name='chapter-detail'),
    path(_('book/<slug:book_slug>/chapter/<slug:chapter_slug>/<slug:section_slug>-<int:section_pk>/'), SectionDetailView.as_view(), name='section-detail'),
    path(_('book/<slug:book_slug>/search/'), SectionSearchView.as_view(), name='section-search'),
    path(_('chapter-autocomplete/'), ChapterAutocomplete.as_view(), name='chapter-autocomplete',),
    path(_('section-autocomplete-book/'), SectionAutocompleteFromProduct.as_view(), name='section-autocomplete-book',),
]