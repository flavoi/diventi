from functools import reduce
import operator

from django.db import models
from django.db.models import Prefetch, Q

from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor.fields import RichTextField
from hitcount.models import HitCount, HitCountMixin

from diventi.core.models import (
    Element,
    TimeStampedModel,
    PublishableModel,
    FeaturedModelQuerySet,
)

from diventi.products.models import (
    Product,
)


class PackageQuerySet(FeaturedModelQuerySet):

    # Prefetch all relevant data
    def prefetch(self):
        packages = self.prefetch_related(Prefetch('related_products', queryset=Product.objects.published()))
        packages = packages.prefetch_related('faq')
        return packages

    # Returns the first pinned package
    def pinned(self):
        package = self.published().filter(pinned=True)
        try:
            package = package.get()
        except Package.MultipleObjectsReturned:
            package = package.order_by('-publication_date').first()
        except Package.DoesNotExist:
            package = package.first()
        return package

    # Return the list of pinned packages
    def pinned_list(self):
        packages = self.published().filter(pinned=True).prefetch()
        return packages


class Package(TimeStampedModel, PublishableModel, Element, HitCountMixin):
    """
        A package contains one or more products and can 
        be used to pubblish special discounts to the final
        customer. 
    """
    description = RichTextField(
        verbose_name = _('description')
    )
    short_description = models.TextField(
        blank=True, 
        max_length=50, 
        verbose_name=_('short description')
    )
    abstract = models.TextField(
        blank=True, 
        max_length=200, 
        verbose_name=_('abstract')
    )
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
    hit_count_generic = GenericRelation(
        HitCount, 
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    ) # Counts the views on this model
    
    objects = PackageQuerySet.as_manager()

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')

    def get_absolute_url(self):
        return reverse('packages:detail', args=[str(self.slug)])

    def search(self, query, *args, **kwargs):
        results = Package.objects.published()
        query_list = query.split()
        results = results.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list))
        )
        return results

    def class_name(self):
        return _('package')

    def get_hitcounts(self):
        return self.hit_count.hits
    get_hitcounts.short_description = _('Hit counts')
    get_hitcounts.admin_order_field = 'hit_count_generic__hits'

    def reporting(self, *args, **kwargs):
        queryset = Package.objects.published()
        results = []
        for package in queryset:
            results.append({
                'columns': 4,
                'name': '%(package)s' % {
                    'package': package.title,
                },
                'title': package.hit_count.hits,
                'description1': _('views in the last week: %(d)s') % {
                    'd': package.hit_count.hits_in_last(days=7),
                },
                'description2': '',
                'action': '',
            })
        return results

    def __str__(self):
        return '{}'.format(self.title)


class FAQ(TimeStampedModel, Element):

    answer = models.TextField(
        verbose_name = _('answer')
    )

    package = models.ForeignKey(
        Package,
        related_name = 'faq',
        on_delete=models.SET_NULL,
        blank = True,
        null = True,
        verbose_name = _('package'),
    )

    class Meta:
        verbose_name = _('faq')
        verbose_name_plural = _('faq')

    def __str__(self):
        return '{}'.format(self.title)

