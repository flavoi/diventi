from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from diventi.ebooks.views import UserHasProductMixin, EbookView

from .models import CharacterSheet


class CharacterSheetDetailView(LoginRequiredMixin, UserHasProductMixin, 
                        EbookView, DetailView):
    """ Returns the digital character sheet. """
    
    model = CharacterSheet
    template_name = "sheets/charactersheet_detail.html"
    slug_url_kwarg = 'character_slug'