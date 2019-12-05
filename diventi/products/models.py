from functools import reduce
import operator
import unicodedata

from django.db import models
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _, gettext

from cuser.middleware import CuserMiddleware

from .fields import ProtectedFileField

from diventi.core.models import Element, DiventiImageModel, TimeStampedModel, PublishableModel, Category


class ProductQuerySet(models.QuerySet):

    # Prefetch all relevant data
    def prefetch(self):
        products = self.prefetch_related('chapters')
        products = products.prefetch_related('authors')
        products = products.prefetch_related('related_products')
        return products

    # Get the available products
    def available(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            products = self
        else:
            products = self.filter(available=True)
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


class ProductCategory(Category):
    """
        Defines the type of a product.
    """
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
    file = ProtectedFileField(upload_to='products/files/', blank=True, verbose_name=_('file'))
    category = models.ForeignKey(ProductCategory, null=True, blank=True, verbose_name=_('category'), default='default', on_delete=models.SET_NULL)
    available = models.BooleanField(default=False, verbose_name=_('available')) # Disable the access to the file
    courtesy_short_message = models.CharField(blank=True, max_length=50, verbose_name=_('short courtesy messages'))
    courtesy_message = models.TextField(blank=True, verbose_name=_('courtesy message')) # Explains why the product is under maintenance
    related_products = models.ManyToManyField(
        'self',
        related_name='related_products', 
        blank=True, 
        verbose_name=_('related products'),
    ) # Connect this product to others
    price = models.PositiveIntegerField(blank=True, verbose_name=_('price'), help_text=_('This price must be valued in euro cents. For example: 500 for 5.00€, 120 for 1.20€ etc.'))

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title

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

    # Return True if the user has added the product to his collections
    def user_has_already_bought(self, user):
        return user in self.buyers.all()

    # Return True if the user has authored this collection
    def user_has_authored(self, user):
        return user in self.authors.all()

    # Checks if this product is available for the buyers
    def is_available(self):
        p = Product.objects.filter(pk=self.pk)
        return p.available().exists()

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
