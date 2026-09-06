from django.core.cache import cache
from .models import Product, ProductCategory

def project_categories(request):
    # Sfruttiamo il metodo visible() senza distruggere il prefetch
    categories = cache.get('global_project_categories')
    if categories is None:
        categories = list(ProductCategory.objects.visible())
        cache.set('global_project_categories', categories, 3600) # Cache per 1 ora
    return {'project_categories': categories}


def pinned_projects(request):
    pinned = cache.get('global_pinned_projects')
    if pinned is None:
        pinned = list(Product.objects.published().hot().prefetch_basic())
        cache.set('global_pinned_projects', pinned, 3600)
    return {'pinned_products_nav': pinned}