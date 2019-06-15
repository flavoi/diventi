import operator
from functools import reduce

from django.db import models
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models import Prefetch, Q

from ckeditor.fields import RichTextField
from cuser.middleware import CuserMiddleware


from diventi.products.models import Product
from diventi.core.models import (
    Element, 
    TimeStampedModel, 
    PublishableModel, 
    DisclosableModel, 
    DiventiImageModel, 
    DiventiColModel
)


class BookQuerySet(models.QuerySet):

    # Get the list of published articles 
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            books = self
        else:
            books = self.filter(published=True)
        return books

    # Fetch the book related to the chapter
    def product(self):
        book = self.select_related('book_product')
        return book


class Book(Element, TimeStampedModel, PublishableModel, DiventiColModel):
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

    # Get the list of published articles 
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            chapters = self
        else:
            chapters = self.filter(chapter_book__published=True)
        return chapters


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
        return '({0}) {1} - {2}'.format(self.order_index, self.chapter_book, self.title)

    def get_absolute_url(self):
        return reverse('ebooks:chapter-detail', args=[self.chapter_book.slug, self.slug])

    objects = ChapterQuerySet.as_manager()

    class Meta:
        verbose_name = _('chapter')
        verbose_name_plural = _('chapters')


class UniversalSection(Element, TimeStampedModel):
    """ A section that can be copied but not published. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    content = RichTextField(blank=True, null=True, verbose_name=_('content'))

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


class Section(Element, TimeStampedModel, DiventiImageModel, DiventiColModel):
    """ A section of a chapter. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    content = RichTextField(verbose_name=_('content'), blank=True)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.SET_NULL, related_name=('sections'), verbose_name=_('chapter'))
    universal_section = models.ForeignKey(UniversalSection, null=True, blank=True, on_delete=models.SET_NULL, related_name=('sections'), verbose_name=_('universal section'))
    DEFAULT_ALIGNMENT = 'left'
    ALIGNMENT_CHOICES = [
        (DEFAULT_ALIGNMENT, _('Left')),
        ('center', _('Center')),
        ('right', _('Right')),
    ]
    text_alignment = models.CharField(max_length=20, choices=ALIGNMENT_CHOICES, default=DEFAULT_ALIGNMENT, verbose_name=_('text alignment'))
    DEFAULT_TEMPLATE = 'section_standard.html'
    TEMPLATE_CHOICES = (
        (DEFAULT_TEMPLATE, _('Standard')),
        ('section_with_icon.html', _('With icon')),
        ('section_with_image.html', _('With image')),
    )
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default=DEFAULT_TEMPLATE, verbose_name=_('template'))
    DEFAULT_CARD_TYPE = ' '
    CARD_TYPES = [
        (DEFAULT_CARD_TYPE, _('Standard')),
        ('card-plain', _('No background')),
    ]
    card_type = models.CharField(max_length=30, choices=CARD_TYPES, default=DEFAULT_CARD_TYPE, verbose_name=_('card type'))
    slug = models.SlugField(unique=True, null=True, verbose_name=_('slug'))

    objects = SectionQuerySet.as_manager()

    def __str__(self):
        return '({0}) {1}'.format(self.order_index, self.title)

    def search(self, query, book_slug, *args, **kwargs):
        book = Book.objects.published().get(slug=book_slug)
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
