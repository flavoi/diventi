import stripe

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from hitcount.views import HitCountDetailView

from diventi.core.utils import (
    humanize_price,
)

from diventi.products.models import Purchase

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
        return qs.published().prefetch()

    def get_context_data(self, **kwargs):
        context = super(PackageDetailView, self).get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        stripe_price = stripe.Price.retrieve(self.object.stripe_price)
        stipe_price = float(stripe_price['unit_amount_decimal'])
        context['price'] = humanize_price(stipe_price)
        related_products = self.object.related_products.all()
        if self.request.user.is_anonymous:
            products_already_bought = Purchase.objects.none()
        else:
            products_already_bought = Purchase.objects.filter(product__in=related_products, customer=self.request.user)
        related_products = related_products.exclude(id__in=products_already_bought.values('product__id'))
        context['products_already_bought'] = products_already_bought.values_list('product__id', flat=True)
        if related_products.exists():
            related_products_prices = [stripe.Price.retrieve(p['stripe_price']) for p in related_products.values('stripe_price')]
            related_products_value = sum([float(v['unit_amount_decimal']) for v in related_products_prices])
            context['related_products_value'] = humanize_price(related_products_value)
            package_discount = round((1 - (stipe_price / related_products_value)) * 100, 2)
            if package_discount > 0:
                context['discount'] = package_discount
        else:
            context['bought'] = 1
        return context

