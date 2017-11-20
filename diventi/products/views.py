from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Product


class ProductDetailView(DetailView):

    model = Product
    context_object_name = 'product'

    # Returns only published articles
    """
    def get_queryset(self):
        qs = super(ArticleDetailView, self).get_queryset()
        return qs.published().promotions()
    """