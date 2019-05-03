import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from ckeditor.fields import RichTextField

from diventi.products.models import Product
from diventi.core.models import Element, TimeStampedModel, PublishableModel, DisclosableModel


class BookQuerySet(models.QuerySet):

    # Fetch the book related to the chapter
    def product(self):
        book = self.select_related('book_product')
        return book


class Book(Element, TimeStampedModel, PublishableModel):
    """ A collection of chapters that constitutes a product. """
    short_title = models.CharField(max_length=2, verbose_name=_('short title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    book_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('product'))

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return '%s' % (self.title)

    def get_product_category(self):
        if self.book_product:
            return self.book_product.category
        else:
            return None
    get_product_category.short_description = _('category')

    def get_product_image(self):
        if self.book_product:
            return self.book_product.image_tag()
        else:
            return None
    get_product_image.short_description = _('image')

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
