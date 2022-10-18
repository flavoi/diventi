from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from diventi.core.models import (
    Element,
    TimeStampedModel,
    PublishableModel,
)

from diventi.products.models import (
    Product,
)


class Package(TimeStampedModel, PublishableModel, Element):
    """
        A package contains one or more products and can 
        be used to pubblish special discounts to the final
        customer. 
    """

    pinned = models.BooleanField(
        default = False,
        verbose_name = _('pinned'),
        help_text = _('Pinned packages appear on the landing page') 
    )
    related_products = models.ManyToManyField(
        Product,
        related_name = 'packages', 
        blank = True, 
        verbose_name = _('related products'),
    )
    stripe_price = models.CharField(
        blank = True,
        max_length = 50,
        verbose_name = _('stripe price')
    )
    stripe_product = models.CharField(
        unique = True,
        null = True,
        blank = True,
        max_length = 50,
        verbose_name = _('stripe product')
    )
    courtesy_short_message = models.CharField(
        max_length=50, 
        verbose_name=_('short courtesy messages')
    )
    courtesy_message = models.TextField(
        verbose_name = _('courtesy message'),
        help_text = _('Folded products return this message to all users')
    )
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('slug')
    )
    
    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')

    def get_absolute_url(self):
        return reverse('packages:detail', args=[str(self.slug)])

    def __str__(self):
        return '{}'.format(self.title)
