"""
    Custom context processors for the products app.
"""

from django.utils import translation
from django.utils.translation import get_language
from django.db.models import Prefetch

from .models import (
    GemmaIstruction,
)


def playable_gemmas(request):
    context = {}
    context['playable_gemmas_nav'] = GemmaIstruction.objects.playable(user=request.user)
    return context