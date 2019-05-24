import operator
from functools import reduce

from django.db import models
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models import Prefetch, Q

from ckeditor.fields import RichTextField

from diventi.products.models import Product
from diventi.core.models import Element, TimeStampedModel, PublishableModel, DisclosableModel, DiventiImageModel


class BookQuerySet(models.QuerySet):

    # Fetch the book related to the chapter
    def product(self):
        book = self.select_related('book_product')
        return book


class Book(Element, TimeStampedModel, PublishableModel):
    """ A collection of chapters that constitutes a product. """
    short_title = models.CharField(max_length=2, verbose_name=_('short title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    book_product = models.OneToOneField(Product, null=True, blank=True, related_name='book', on_delete=models.SET_NULL, verbose_name=_('product'))

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return '%s' % (self.title)

    def get_absolute_url(self):
        return reverse('ebooks:book-detail', args=[self.slug])

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
        chapter = self.prefetch_related(Prefetch('sections', queryset=Section.objects.usection().order_by('order_index')))
        return chapter


class Chapter(Element, TimeStampedModel, PublishableModel):
    """ A chapter of a book. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    chapter_book = models.ForeignKey(Book, null=True, blank=True, related_name='chapters', on_delete=models.SET_NULL, verbose_name=_('book'))

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    def get_absolute_url(self):
        return reverse('ebooks:chapter-detail', args=[self.chapter_book.slug, self.slug])

    objects = ChapterQuerySet.as_manager()

    class Meta:
        verbose_name = _('chapter')
        verbose_name_plural = _('chapters')


class UniversalSection(Element, TimeStampedModel):
    """ A section that can be copied but not published. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    content = RichTextField(verbose_name=_('content'))

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    def get_universal_chapter(self):
        return _('universal Diventi')
    get_universal_chapter.short_description = _('chapter')

    class Meta:
        verbose_name = _('universal Section')
        verbose_name_plural = _('universal Sections')


class SectionQuerySet(models.QuerySet):

    # Fetch the universal section related to the section
    def usection(self):
        section = self.select_related('universal_section')
        return section


class Section(Element, TimeStampedModel, DiventiImageModel):
    """ A section of a chapter. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    content = RichTextField(verbose_name=_('content'), blank=True)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.SET_NULL, related_name=('sections'), verbose_name=_('chapter'))
    universal_section = models.ForeignKey(UniversalSection, null=True, blank=True, on_delete=models.SET_NULL, related_name=('sections'), verbose_name=_('universal section'))
    COL_CHOICES = [
        (12, _('Full')),
        (6, _('Half')),
        (4, _('Quarter')),
    ]
    col_lg = models.PositiveIntegerField(default=12, choices=COL_CHOICES, verbose_name=_('lg column'))
    col_md = models.PositiveIntegerField(default=12, choices=COL_CHOICES, verbose_name=_('md column'))
    ALIGNMENT_CHOICES = [
        ('left', _('Left')),
        ('center', _('Center')),
        ('right', _('Right')),
    ]
    text_alignment = models.CharField(default='left', max_length=20, choices=ALIGNMENT_CHOICES, verbose_name=_('text alignment'))
    super_title = models.BooleanField(default=False, verbose_name=_('super title'))

    objects = SectionQuerySet.as_manager()

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    def search(self, query, book_slug, *args, **kwargs):
        book = Book.objects.get(slug=book_slug)
        results = Section.objects.filter(chapter__chapter_book=book)
        query_list = query.split()
        results = results.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list))
        )
        return results

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
