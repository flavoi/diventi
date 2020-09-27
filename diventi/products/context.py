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
    projects = ProductCategory.objects.visible()
    # chapter = self.prefetch_related(Prefetch('sections', queryset=Section.objects.usection()))
    projects = projects.prefetch_related(Prefetch('projects', queryset=Product.objects.published()))
    context['projects'] = projects
    return context
