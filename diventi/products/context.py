"""
    Custom context processors for the products app.
"""

from django.utils import translation
from django.utils.translation import get_language

from .models import (
	Product,
	ProductCategory,
)


def projects(request):
    context = {}
    projects = ProductCategory.objects.visible()
    context['projects'] = projects
    return context