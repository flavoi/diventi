from functools import reduce
import operator
import unicodedata

from django.db import models
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _, gettext
from django.contrib.humanize.templatetags.humanize import naturalday

from cuser.middleware import CuserMiddleware

from .fields import ProtectedFileField

from diventi.core.models import Element, DiventiImageModel, TimeStampedModel, PublishableModel, Category


class ProductQuerySet(models.QuerySet):

    # Prefetch all relevant data
    def prefetch(self):
        products = self.prefetch_related('chapters')
        products = products.prefetch_related('authors')
        products = products.prefetch_related('related_products')
        products = products.prefetch_related('customers')
        return products

    # Fetch the products authored or purchased by the user
    def user_collection(self, user):
        if user.is_anonymous:
            products = self.none()
        else:
            products = self.filter(buyers=user)
        if user.is_staff:
            authored_products = self.filter(authors=user)
            products = products.union(authored_products)
        products = products.prefetch()
        return products

    # Get the featured products that are included in the user collection
    def featured(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            products = self
        else:
            products = self.filter(featured=True) 
            products = products.user_collection(user)
        return products

    # Get all the published products 
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            products = self
        else:
            products = self.filter(published=True)
        products = products.prefetch()
        return products

    # Returns the users that purchased the product
    # with "lan" as main language
    def customers(self, lan):
        product = self.get()
        customers = product.customers.all()
        customers = customers.filter(language=lan)
        customers = customers.is_active()
        return customers

    # Returns the emails of users that purchased the product
    # with "lan" as main language
    def customers_emails(self, lan):
        customers = self.customers(lan)
        customers = customers.has_agreed_gdpr()
        customers = customers.values_list('email', flat=True)
        return customers


class ProductCategory(Category):
    """
        Defines the type of a product.
    """
    meta_category = models.BooleanField(default=False, verbose_name=_('meta category'))

    class Meta:
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')


class Product(TimeStampedModel, PublishableModel, DiventiImageModel):
    """ An adventure or a module published by Diventi. """
    title = models.CharField(max_length=50, verbose_name=_('title'))
    abstract = models.TextField(blank=True, max_length=200, verbose_name=_('abstract'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    featured = models.BooleanField(default=False, verbose_name=_('featured'))
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='products', verbose_name=_('authors'))
    buyers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collection', blank=True, verbose_name=_('buyers'))
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Purchase', blank=True, verbose_name=_('customers'))
    file = ProtectedFileField(upload_to='products/files/', blank=True, verbose_name=_('file'))
    category = models.ForeignKey(ProductCategory, null=True, blank=True, verbose_name=_('category'), default='default', on_delete=models.SET_NULL)
    courtesy_short_message = models.CharField(blank=True, max_length=50, verbose_name=_('short courtesy messages'))
    courtesy_message = models.TextField(blank=True, verbose_name=_('courtesy message')) # Explains why the product is under maintenance
    related_products = models.ManyToManyField(
        'self',
        related_name='related_products', 
        blank=True, 
        verbose_name=_('related products'),
    ) # Connect this product to others
    price = models.PositiveIntegerField(default=0, verbose_name=_('price'), help_text=_('This price must be valued in euro cents. For example: 500 for 5.00€, 120 for 1.20€ etc.'))

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return '{} ({})'.format(self.title, self.category) 

    def class_name(self):
        return _('application')

    def get_absolute_url(self):
        return reverse('products:detail', args=[str(self.slug)])

    def get_lazy_absolute_url(self):
        return reverse_lazy('products:detail', args=[str(self.slug)])

    def search(self, query, *args, **kwargs):
        results = Product.objects.published()
        query_list = query.split()
        results = results.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list))
        )
        return results

    def reporting(self, *args, **kwargs):
        queryset = Product.objects.all().exclude(category__meta_category=True)
        queryset = queryset.prefetch()
        results = []
        for product in queryset:
            results.append({
                'name': _('%(product)s: total customers') % {
                    'product': product.title,
                },
                'title': product.customers.count(),
                'description': _('%(en)s english customers, %(it)s italian customers') % {
                    'en': product.get_customers_emails('it').count(),
                    'it': product.get_customers_emails('en').count(),
                },
                'action': '',
            })
            last_purchase = Purchase.objects.last_purchase(product, 'en')
            prefix = _('Last purchase')
            results.append({
                'name': _('%(product)s: english gdpr customers') % {
                    'product': product.title,
                },
                'title': product.get_customers_emails('en').count(),
                'description': last_purchase.get_description(prefix) if last_purchase is not None else prefix + ': -',
                'action': {'label': _('copy emails'), 'function': 'copy-emails', 'parameters': product.get_customers_emails('en')},
            })
            last_purchase = Purchase.objects.last_purchase(product, 'it')
            results.append({
                'name': _('%(product)s: italian gdpr customers') % {
                    'product': product.title,
                },
                'title': product.get_customers_emails('it').count(),
                'description': last_purchase.get_description(prefix) if last_purchase is not None else prefix + ': -',
                'action': {'label': _('copy emails'), 'function': 'copy-emails', 'parameters': product.get_customers_emails('it')},
            })
        return results

    # Return True if the user has added the product to his collections
    def user_has_already_bought(self, user):
        return user in self.customers.all()

    # Return True if the user has authored this collection
    def user_has_authored(self, user):
        return user in self.authors.all()

    # Check if this product can be reviewed by the user
    def is_published(self):
        p = Product.objects.filter(pk=self.pk)
        return p.published().exists()

    # Returns the price of the product
    def get_price(self):
        p = ('%(currency)s %(price).2f' % {
            'currency': unicodedata.lookup('EURO SIGN'), 
            'price': self.price / 100,
        })
        return p

    # Get the emails of this product buyers
    def get_customers_emails(self, lan):
        p = Product.objects.filter(pk=self.pk)
        p = p.customers_emails(lan)
        return p

    # Returns the publishable status of the product
    def get_status(self): 
        if self.published:
            return _('published')
        else:
            return _('draft')


class ChapterCategory(Category):
    """
        Defines the type of a chapter.
    """
    class Meta:
        verbose_name = _('Chapter category')
        verbose_name_plural = _('Chapter categories')


class Chapter(Element, DiventiImageModel):
    """ A specific detail of a product."""
    product = models.ForeignKey(Product, null=True, related_name='chapters', verbose_name=_('product'), on_delete=models.SET_NULL)     
    category = models.ForeignKey(ChapterCategory, null=True, verbose_name=_('category'), on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')


class ImagePreview(DiventiImageModel):    
    """A list of cool images of the product."""
    product = models.ForeignKey(Product, null=True, related_name='imagepreviews', verbose_name=_('product'), on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class PurchaseQuerySet(models.QuerySet):

    # Prefetch all relevant data
    def related(self):
        purchases = self.select_related('customer')
        purchases = purchases.select_related('product')
        return purchases

    # Returns the last customer that has purchased the product
    # with "lan" as main language
    def last_purchase(self, product, lan):
        purchases = self.related()
        purchases = purchases.filter(product=product)
        purchases = purchases.filter(customer__language=lan)
        last_purchase = purchases.order_by('-created').first()
        return last_purchase


class Purchase(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = PurchaseQuerySet.as_manager()

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')


    def __str__(self):
        return _('Purchase: %(id)s') % {'id': self.id}

    # Returns the description of the purchase
    # Or none if none is found
    def get_description(self, prefix):
        description = _('%(prefix)s: %(last_pur)s on %(created)s (GDPR: %(gdpr)s)') % {
            'prefix': prefix,
            'last_pur': self.customer.get_short_name(),
            'created': naturalday(self.created),
            'gdpr': _('Yes') if self.customer.has_agreed_gdpr else _('No'),
        }
        return description