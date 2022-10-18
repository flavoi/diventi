import stripe

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from diventi.core.utils import (
    humanize_price,
)

from .models import (
    Package,
)



class PackageDetailView(DetailView):
    """
        Renders the package contents.
    """
    model = Package
    context_object_name = 'package'
    template_name = 'packages/package_detail_quick.html'

    def get_context_data(self, **kwargs):
        context = super(PackageDetailView, self).get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        stripe_price = stripe.Price.retrieve(self.object.stripe_price)
        context['price'] = humanize_price(float(stripe_price['unit_amount_decimal']))
        related_products = self.object.related_products.all()
        related_products_values = [stripe.Price.retrieve(p['stripe_price']) for p in related_products.values('stripe_price')]
        context['related_products_value'] = humanize_price(sum([float(v['unit_amount_decimal']) for v in related_products_values]))
        for product in related_products:
            if (product.user_has_already_bought(self.request.user) or product.user_has_authored(self.request.user)):
                context['bought'] = 1
        return context

