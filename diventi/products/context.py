"""
    Custom context processors for the products app.
"""

from django.utils import translation
from django.utils.translation import get_language
from django.db.models import Prefetch

from .models import (
	Product,
	ProductCategory,
)


def projects(request):
    context = {}
    project_categories = ProductCategory.objects.prefetch_related(Prefetch('projects', queryset=Product.objects.published()))
    project_categories = ProductCategory.objects.visible().distinct()
    context['project_categories'] = project_categories
    return context