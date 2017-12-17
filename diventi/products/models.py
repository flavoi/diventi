from functools import reduce
import operator

from django.db import models
from django.db.models import Q
from django.urls import reverse

from diventi.core.models import Element, DiventiImageModel


class ProductQuerySet(models.QuerySet):
    
    # Get all the published products 
    def published(self):
        products = self.filter(published=True)
        return products

    # Get the featured product that appears on the landing page 
    def featured(self):
        try:
            featured_product = self.prefetch_related('events')
            featured_product = featured_product.prefetch_related('chapters')
            featured_product = featured_product.prefetch_related('characteristics')
            featured_product = featured_product.published().get(featured=True) 
        except Product.DoesNotExist:
            # Fail silently, return nothing
            featured_product = self.none() 
        except Product.MultipleObjectsReturned:
            msg = 'Multiple featured products returned. Please fix!'
            raise Product.MultipleObjectsReturned(msg)        
        return featured_product


class Product(models.Model):
    """ An adventure or a module published by Diventi. """
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=False)
    cover = models.ImageField(blank=True, upload_to='products/')
    published = models.BooleanField(default=False)

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

class Event(Element):
    """ An element of the timeline that describes the incipit of the adventure."""
    product = models.ForeignKey(Product, related_name='events')
    event_date = models.DateField(blank=True)

    class Meta:
        ordering = ['event_date']


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




