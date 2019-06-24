from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import CharacterSheetDetailView

app_name = 'sheets'

urlpatterns = [
    path(_('character/<int:pk>/book/<slug:book_slug>'), CharacterSheetDetailView.as_view(), name='charactersheet-detail'),
]