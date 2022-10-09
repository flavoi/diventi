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


def project_categories(request):
    context = {}
    project_categories = ProductCategory.objects.prefetch_related(Prefetch('projects', queryset=Product.objects.published()))
    project_categories = ProductCategory.objects.visible().distinct()
    context['project_categories'] = project_categories
    return context


def pinned_projects(request):
    context = {}
    pinned_projects = (Product.objects.hot() | Product.objects.pinned_list()).distinct()
    context['pinned_projects'] = pinned_projects
    return context