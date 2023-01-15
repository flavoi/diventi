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
    context['pinned_products_nav'] = Product.objects.pinned_list().distinct()
    try:
        context['hot_product_nav'] = Product.objects.hot().get()
    except Product.DoesNotExist:
        context['hot_product_nav'] = None
    return context