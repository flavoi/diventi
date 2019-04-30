import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from ckeditor.fields import RichTextField

from diventi.products.models import Product
from diventi.core.models import Element, TimeStampedModel, PublishableModel, DisclosableModel


class Book(Element, TimeStampedModel, PublishableModel):
    """ A collection of chapters that constitutes a product. """
    short_title = models.CharField(max_length=2, verbose_name=_('short title'))
    category = models.CharField(max_length=100, verbose_name=_('category'), blank=True)
    slug = models.SlugField(unique=True, verbose_name=_('slug'))

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')


class ChapterQuerySet(models.QuerySet):

    # Fetch all the sections related to the chapter
    def sections(self):
        chapter = self.prefetch_related('sections')
        return chapter


class Chapter(Element, TimeStampedModel, PublishableModel):
    """ A chapter of a book. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    chapter_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('product'))
    chapter_book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('book'))

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    def get_absolute_url(self):
        return reverse('ebooks:chapter-detail', args=[self.chapter_book.slug, self.slug])

    objects = ChapterQuerySet.as_manager()

    class Meta:
        verbose_name = _('chapter')
        verbose_name_plural = _('chapters')


class Section(Element, TimeStampedModel):
    """ A section of a chapter. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    content = RichTextField(verbose_name=_('content'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.SET_NULL, related_name=('sections'), verbose_name=_('chapter'))

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
