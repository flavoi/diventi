import stripe

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from hitcount.views import HitCountDetailView

from diventi.core.utils import (
    humanize_price,
)

from .models import (
    Package,
)


class PackageDetailView(HitCountDetailView):
    """
        Renders the package contents.
    """
    model = Package
    count_hit = True
    context_object_name = 'package'
    template_name = 'packages/package_detail_quick.html'

    def get_queryset(self):
        qs = super(PackageDetailView, self).get_queryset()
        return qs.prefetch()

    def get_context_data(self, **kwargs):
        context = super(PackageDetailView, self).get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        stripe_price = stripe.Price.retrieve(self.object.stripe_price)
        stipe_price = float(stripe_price['unit_amount_decimal'])
        context['price'] = humanize_price(stipe_price)
        related_products = self.object.related_products.all()
        relate_products_prices = [stripe.Price.retrieve(p['stripe_price']) for p in related_products.values('stripe_price')]
        related_products_value = sum([float(v['unit_amount_decimal']) for v in relate_products_prices])
        context['related_products_value'] = humanize_price(related_products_value)
        context['package_discount'] = round((stipe_price / related_products_value) * 100, 2)
        for product in related_products:
            if (product.user_has_already_bought(self.request.user) or product.user_has_authored(self.request.user)):
                context['bought'] = 1
        return context

