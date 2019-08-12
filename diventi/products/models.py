from functools import reduce
import operator

from django.db import models
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from cuser.middleware import CuserMiddleware

from .fields import ProtectedFileField

from diventi.core.models import Element, DiventiImageModel, TimeStampedModel, PublishableModel, Category


class ProductQuerySet(models.QuerySet):
    
    # Get all the published products 
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            products = self
        else:
            products = self.filter(published=True)
        products = products.prefetch_related('chapters')
        products = products.prefetch_related('authors')
        products = products.prefetch_related('related_products')
        return products

    # Get the available products
    def available(self):
        products = self.published()
        if user.is_superuser:
            products = self
        else:
            products = self.filter(available=True)
        return products

    # Get the featured product 
    def featured(self):
        try:
            featured_product = featured_product.published().get(featured=True) 
        except Product.DoesNotExist:
            # Fail silently, return nothing
            featured_product = self.none() 
        except Product.MultipleObjectsReturned:
            msg = _('Multiple featured products returned. Please fix!')
            raise Product.MultipleObjectsReturned(msg)        
        return featured_product

    # Fetch the products authored or purchased by the user
    def user_collection(self, user):
        products = self.filter(buyers=user)
        if user.is_staff:
            authored_products = self.filter(authors=user)
            products = products.union(authored_products)
        products = products.prefetch_related('book')
        products = products.prefetch_related('authors')
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
    courtesy_short_message = models.CharField(max_length=50, verbose_name=_('short courtesy messages'))
    courtesy_message = models.TextField(verbose_name=_('courtesy message')) # Explains why the product is under maintenance
    related_products = models.ManyToManyField(
        'self',
        related_name='related_products', 
        blank=True, 
        verbose_name=_('related products'),
    ) # Connect this product to others

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
