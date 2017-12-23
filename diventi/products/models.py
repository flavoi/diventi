from functools import reduce
import operator

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.conf import settings

from diventi.core.models import Element, DiventiImageModel, TimeStampedModel, PublishableModel


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
            msg = 'Multiple featured products returned. Please fix!'
            raise Product.MultipleObjectsReturned(msg)        
        return featured_product

    # Fetch the products authored or purchased by the user
    def user_collection(self, user):
        if user.is_staff: # User is a creator
            products = self.filter(authors=user)
        else:
            products = self.filter(buyers=user)
        return products


class Product(TimeStampedModel, PublishableModel):
    """ An adventure or a module published by Diventi. """
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=False)
    cover = models.ImageField(blank=True, upload_to='products/')
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='products')
    buyers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collection', blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.title

    def class_name(self):
        return self.__class__.__name__

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


class Chapter(Element, DiventiImageModel):
    """ A stand-alone chapter of an adventure."""
    product = models.ForeignKey(Product, related_name='chapters')     


class Characteristic(Element):
    """ A specific detail of a product."""
    product = models.ForeignKey(Product, related_name='characteristics')


class ImagePreview(DiventiImageModel):    
    """A list of cool images of the product."""
    product = models.ForeignKey(Product, related_name='imagepreviews')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'




