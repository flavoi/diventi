from functools import reduce
import operator

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from diventi.core.models import Element, DiventiImageModel, TimeStampedModel, PublishableModel, Category


class ProductQuerySet(models.QuerySet):
    
    # Get all the published products 
    def published(self):
        products = self.filter(published=True)
        return products

    # Get the featured product that appears on the landing page 
    def featured(self):
        try:
            featured_product = self.prefetch_related('chapters')
            featured_product = featured_product.prefetch_related('characteristics')
            featured_product = featured_product.prefetch_related('authors')
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
        if user.is_staff: # User is a creator
            products = self.filter(authors=user)
        else:
            products = self.filter(buyers=user)
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
    description = models.TextField(blank=True, verbose_name=_('description'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    featured = models.BooleanField(default=False, verbose_name=_('featured'))    
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='products', verbose_name=_('authors'))
    buyers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collection', blank=True, verbose_name=_('buyers'))
    file = models.FileField(upload_to='products/files/', blank=True, verbose_name=_('file'))
    category = models.ForeignKey(ProductCategory, null=True, blank=True, verbose_name=_('category'))
    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.title

    def class_name(self):
        return _('product')

    def get_absolute_url(self):
        return reverse('products:detail', args=[str(self.slug)])

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

    # Check if the user has added the product to its collections
    def user_has_already_bought(self, user):
        return user in self.buyers.all()


class ChapterCategory(Category):
    """
        Defines the type of a chapter.
    """
    class Meta:
        verbose_name = _('Chapter category')
        verbose_name_plural = _('Chapter categories')


class Chapter(Element, DiventiImageModel):
    """ A stand-alone chapter of an adventure."""
    product = models.ForeignKey(Product, related_name='chapters', verbose_name=_('product'))     
    category = models.ForeignKey(ChapterCategory, null=True, blank=True, verbose_name=_('category'))

    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')


class Characteristic(Element):
    """ A specific detail of a product."""
    product = models.ForeignKey(Product, related_name='characteristics', verbose_name=_('product'))

    class Meta:
        verbose_name = _('Characteristic')
        verbose_name_plural = _('Characteristics')

class ImagePreview(DiventiImageModel):    
    """A list of cool images of the product."""
    product = models.ForeignKey(Product, related_name='imagepreviews', verbose_name=_('product'))

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')




