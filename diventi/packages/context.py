"""
    Custom context processors for the packages app.
"""

from .models import (
    Package,
)


def pinned_packages(request):
    context = {}
    context['pinned_packages'] = Package.objects.pinned_list()
    return context