import operator, re
from functools import reduce

from django.db import models
from django.db.models import Prefetch, Q
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import capfirst
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor.fields import RichTextField
from cuser.middleware import CuserMiddleware
from hitcount.models import HitCount, HitCountMixin

from diventi.products.models import Product
from diventi.core.models import (
    Element, 
    TimeStampedModel, 
    PublishableModel, 
    DiventiImageModel, 
    DiventiColModel
)


class AbstractSection(Element, TimeStampedModel):
    description = RichTextField(
        blank=True, 
        verbose_name=_('description'),
        help_text=_('This content will appear as a brief tooltip thought the book.')
    )

    class Meta:
        abstract = True


class BookQuerySet(models.QuerySet):

    # Get the list of published articles
    # It always returns the book if the user is super or author.
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            books = self
        else:
            books = self.filter(published=True)
        return books

    # Fetch the book related to the chapter
    def product(self):
        book = self.select_related('book_product')
        return book


class Part(Element):
    pass

    class Meta:
        verbose_name = _('part')
        verbose_name_plural = _('parts')


class Book(Element, DiventiImageModel, TimeStampedModel, PublishableModel, DiventiColModel, HitCountMixin):
    """ A collection of chapters that constitutes a product. """
    short_title = models.CharField(max_length=2, verbose_name=_('short title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    book_product = models.OneToOneField(
        Product, 
        null = True, 
        blank = True, 
        related_name = 'book', 
        on_delete = models.SET_NULL, 
        verbose_name = _('product'),
    )
    summary = RichTextField(
        blank = True,
        verbose_name = _('summary'),
    )
    # The unique ID that points to the dropbox paper document
    paper_id = models.CharField(
        max_length = 50,
        blank = True,
        null = True,
        verbose_name = _('paper id')
    )
    legacy_paper_id = models.CharField(
        max_length = 50,
        blank = True,
        null = True,
        verbose_name = _('legacy paper id')
    )
    content_file_url = models.URLField(
        blank=True, 
        verbose_name = _('file url'),
    )
    logo = models.URLField(
        blank=True, 
        verbose_name = _('logo'),
    )
    hit_count_generic = GenericRelation(
        HitCount, 
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    ) # Counts the views on this model
    continuous_update = models.BooleanField(
        default = False,
        verbose_name = _('continuous update')
    )

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return '%s' % (self.title)

    def get_absolute_url(self):
        if self.content_file_url:
            return reverse('ebooks:pdf-detail', args=[self.slug,])
        else:    
            return reverse('ebooks:book-detail', args=[self.slug,])

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

    def get_logo_image(self):
        if self.logo:
            return mark_safe('<img style="max-width:250px;" src="{0}" />'.format(self.logo))
        else:
            return _('No image')
    get_logo_image.short_description = _('logo')

    # Check if this book can be read by the user
    def is_published(self):
        b = Book.objects.filter(pk=self.pk)
        return b.published().exists()

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def get_hitcounts(self):
        return self.hit_count.hits
    get_hitcounts.short_description = _('Hit counts')
    get_hitcounts.admin_order_field = 'hit_count_generic__hits'


class ChapterQuerySet(models.QuerySet):

    # Fetch all the sections related to the chapter
    def sections(self):
        chapter = self.prefetch_related(Prefetch('sections', queryset=Section.objects.usection()))
        return chapter

    # Fetch the sections that are also bookmarks
    def bookmark_sections(self):
        chapter = self.prefetch_related(Prefetch('sections', queryset=Section.objects.bookmarks()))
        return chapter

    # Fetch the book related to the chapter
    def book(self):
        chapter = self.select_related('chapter_book')
        return chapter

    # Get the list of published articles 
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            chapters = self
        else:
            chapters = self.filter(chapter_book__published=True)
        chapters = chapters.book() 
        return chapters


class Chapter(Element, DiventiImageModel, TimeStampedModel, PublishableModel):
    """ A chapter of a book. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    slug = models.SlugField(verbose_name=_('slug'))
    chapter_book = models.ForeignKey(Book, null=True, blank=True, related_name='chapters', on_delete=models.SET_NULL, verbose_name=_('book'))
    part = models.ForeignKey(Part, null=True, related_name='parts', on_delete=models.SET_NULL, verbose_name=_('part'))
    updated = models.BooleanField(
        default=False,
        verbose_name=_('updated'),
    )
    new = models.BooleanField(
        default=False,
        verbose_name=_('new'),
    ) 

    def __str__(self):
        return '({0}) {1} - {2}'.format(self.order_index, self.chapter_book, self.title)

    def get_absolute_url(self):
        return reverse('ebooks:chapter-detail', args=[self.chapter_book.slug, self.slug])

    def clean(self):
        # Don't allow the same slug in the same book.
        slug_error_message = _('There cannot be two or more chapter with the same slug in %(book)s.') % {
            'book': self.chapter_book,
        }
        # Italian slug
        if self.chapter_book and self.slug_it:
            same_slug_chapter = Chapter.objects.filter(chapter_book=self.chapter_book, slug_it=self.slug_it)
            same_slug_chapter = same_slug_chapter.count()
            if same_slug_chapter > 1:
                raise ValidationError({'slug_it': slug_error_message})
        # English slug
        if self.chapter_book and self.slug_en:
            same_slug_chapter = Chapter.objects.filter(chapter_book=self.chapter_book, slug_en=self.slug_en)
            same_slug_chapter = same_slug_chapter.count()
            if same_slug_chapter > 1:
                raise ValidationError({'slug_en': slug_error_message })
        
    objects = ChapterQuerySet.as_manager()

    class Meta:
        verbose_name = _('chapter')
        verbose_name_plural = _('chapters')
        ordering = ['-order_index']
        

class UniversalSection(AbstractSection):
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


class ReplacementRule(Element):
    """ Contains the rules that trigger specific strings replacements. """
    initial_string = models.CharField(max_length=30, verbose_name=_('initial string'))
    result_string = models.CharField(max_length=30, verbose_name=_('result string'))    

    class Meta:
        verbose_name = _('replacement rule')
        verbose_name_plural = _('replacement rules')


class SectionQuerySet(models.QuerySet):

    # Fetch the related objects attached to the section
    def usection(self):
        sections = self.select_related('universal_section')
        sections = sections.prefetch_related('rules')
        sections = sections.select_related('chapter')
        sections = sections.prefetch_related(Prefetch('aspects', queryset=SectionAspect.objects.order_by('aspect_type')))
        sections = sections.prefetch_related(Prefetch('secrets', queryset=Secret.objects.order_by('secret_type')))
        sections = sections.order_by('order_index')
        return sections

    # Fetch the section that are also bookmarks
    def bookmarks(self):
        sections = self.usection()
        sections = sections.filter(bookmark=True)
        sections = sections.order_by('order_index')
        return sections


class Section(AbstractSection, DiventiImageModel, DiventiColModel):
    """ A section of a chapter. """
    order_index = models.PositiveIntegerField(
        verbose_name=_('order index')
    )
    content = RichTextField(
        blank=True, 
        verbose_name=_('content'),
        help_text=_('This content should be simple to read aloud by our fellow game masters.')
    )
    situation = RichTextField(
        blank=True, 
        verbose_name=_('situation'),
        help_text=_('This content should be read by game master\'s eyes only.')
    )
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.SET_NULL, related_name=('sections'), verbose_name=_('chapter'))
    bookmark = models.BooleanField(default=True, verbose_name=_('bookmark'))
    universal_section = models.ForeignKey(UniversalSection, null=True, blank=True, on_delete=models.SET_NULL, related_name=('sections'), verbose_name=_('universal section'))
    DEFAULT_ALIGNMENT = 'left'
    ALIGNMENT_CHOICES = [
        (DEFAULT_ALIGNMENT, _('Left')),
        ('center', _('Center')),
        ('right', _('Right')),
    ]
    text_alignment = models.CharField(max_length=20, choices=ALIGNMENT_CHOICES, default=DEFAULT_ALIGNMENT, verbose_name=_('text alignment'))
    rules = models.ManyToManyField(ReplacementRule, blank=True, verbose_name=_('rules'))
    slug = models.SlugField(null=True, verbose_name=_('slug'))

    objects = SectionQuerySet.as_manager()

    def __str__(self):
        return '({0}) {1}'.format(self.order_index, self.title)

    def get_absolute_url(self):
        return reverse('ebooks:section-detail', args=[self.chapter.chapter_book.slug, self.chapter.slug, self.slug, self.pk])

    def get_rules(self):
        return mark_safe("<br>".join([a.title for a in self.rules.all()]))
    get_rules.short_description = _('rules')

    def search(self, query, book_slug, *args, **kwargs):
        book = Book.objects.published().get(slug=book_slug)
        results = Section.objects.filter(chapter__chapter_book=book).usection()
        query_list = query.split()
        results = results.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list))
        )
        return results

    def get_converted_content(self):
        """
            Replace the content of the section according
            to the defined rules.
        """
        usection = ''
        if self.universal_section:
            usection = self.universal_section.content
        content = usection + self.content
        rules = self.rules.all()
        for r in rules:
            content = re.sub(r"\b%s\b" % r.initial_string, r.result_string, content)
            content = re.sub(r"\b%s\b" % capfirst(r.initial_string), capfirst(r.result_string), content)
        return content

    def get_converted_description(self):
        """
            Replace the description of the section according
            to the defined rules.
        """
        usection = ''
        if self.universal_section:
            usection = self.universal_section.description
        description = usection + self.description
        rules = self.rules.all()
        for r in rules:
            description = re.sub(r"\b%s\b" % r.initial_string, r.result_string, description)
            description = re.sub(r"\b%s\b" % capfirst(r.initial_string), capfirst(r.result_string), description)
        return description


    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
        ordering = ['-order_index']


class SectionAspect(Element):
    ASPECT_TYPE_CHOICES = [
        ('location', _('Location aspects')),
        ('adventure', _('Adventure aspects')),
        ('campaign', _('Campaign aspects')),
    ]
    aspect_type = models.CharField(
        max_length=20, 
        choices=ASPECT_TYPE_CHOICES, 
        verbose_name=_('aspect type'),
    )
    section = models.ForeignKey(
        Section,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='aspects',
        verbose_name=_('section')
    )

    class Meta:
        verbose_name = _('section aspect')
        verbose_name_plural = _('section aspects')


class Secret(Element):
    SECRET_TYPE_CHOICES = [
        ('treasure', _('Treasure')),
        ('trap', _('Trap')),
        ('revelation', _('Revelation')),
    ]
    secret_type = models.CharField(
        max_length=20, 
        choices=SECRET_TYPE_CHOICES, 
        verbose_name=_('sercret type'),
    )
    section = models.ForeignKey(
        Section,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='secrets',
        verbose_name=_('section')
    )
    requires_skill_check = models.BooleanField(
        default=True,
        verbose_name=_('requires a skill check')
    )

    class Meta:
        verbose_name = _('secret')
        verbose_name_plural = _('secrets')