from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.html import mark_safe
from django.urls import reverse
from django.db.models import Prefetch
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist

from cuser.middleware import CuserMiddleware
from ckeditor.fields import RichTextField
from hitcount.models import HitCount, HitCountMixin

from diventi.core.models import (
    Element, 
    DiventiImageModel, 
    FeaturedModel, 
    FeaturedModelQuerySet,
    FeaturedModelManager,
    SectionModel,
    PublishableModel,
    PublishableModelQuerySet,
    TimeStampedModel,
    PromotableModel,
)

from diventi.accounts.models import DiventiUser
from diventi.products.models import (
    Product,
    ProductCategory,
)
from diventi.feedbacks.models import Survey
from diventi.blog.models import (
    Article,
    ArticleCategory,
)


class AboutArticleQuerySet(PublishableModelQuerySet):

    # Get the published articles, counted by django hitcount
    def hit_count(self):
        articles = self.published().order_by('-hit_count_generic__hits')
        return articles

    # Get the most viewed articles, counted by django hitcount
    def popular(self):
        articles = self.hit_count()[:3]
        return articles


class AboutArticle(TimeStampedModel, PublishableModel, Element, HitCountMixin):
    content = RichTextField(
        verbose_name=_('content')
    )
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('slug')
    )
    hit_count_generic = GenericRelation(
        HitCount, 
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    ) # Counts the views on this model

    objects = AboutArticleQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('landing:about', args=[str(self.slug,)])

    def get_hitcounts(self):
        return self.hit_count.hits
    get_hitcounts.short_description = _('Hit counts')
    get_hitcounts.admin_order_field = 'hit_count_generic__hits'

    def reporting(self, *args, **kwargs):
        queryset = AboutArticle.objects.popular()
        results = []
        for article in queryset:
            results.append({
                'columns': 4,
                'name': '%(article)s' % {
                    'article': article.title,
                },
                'title': article.hit_count.hits,
                'description1': _('views in the last week: %(d)s') % {
                    'd': article.hit_count.hits_in_last(days=7),
                },
                'description2': '',
                'action': '',
            })
        return results

    class Meta:
        verbose_name = _('about article')
        verbose_name_plural = _('about articles')


class PolicyArticle(TimeStampedModel, PublishableModel, Element):
    content = RichTextField(verbose_name=_('content'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))

    def get_absolute_url(self):
        return reverse('landing:policy', args=[str(self.slug,)])

    class Meta:
        verbose_name = _('policy article')
        verbose_name_plural = _('policy article')    


class SectionModelQuerySet(FeaturedModelQuerySet):

    def prefetch(self):
        sections = self.select_related('cover_primary')
        sections = self.select_related('cover_secondary')
        sections = sections.select_related('attached_product')
        sections = sections.select_related('attached_section')
        sections = sections.prefetch_related('attached_section__features')
        sections = sections.prefetch_related('features')
        return sections

    # Get the not featured object that can be selected to appear on the landing page
    def not_featured(self):
        sections = self.filter(featured=False)
        sections = sections.order_by('order_index')
        return sections


class SectionModelManager(FeaturedModelManager):

    def get_queryset(self):
        return SectionModelQuerySet(self.model, using=self._db)

    def not_featured(self):
        return self.get_queryset().not_featured()


class SectionImage(DiventiImageModel):

    class Meta:
        verbose_name = _('section image')
        verbose_name_plural = _('section images')


class Section(DiventiImageModel, FeaturedModel, SectionModel):
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('slug'),
    )
    prefix = models.TextField(
        blank=True, 
        verbose_name=_('prefix text')
    )
    title = models.CharField(
        max_length=50, 
        verbose_name=_('title')
    )
    subtitle = models.CharField(
        blank=True, 
        max_length=50, 
        verbose_name=_('subtitle')
    )
    description = models.TextField(
        blank=True, 
        verbose_name=_('description')
    )
    button_label = models.CharField(
        blank=True, 
        max_length=50, 
        verbose_name=_('button label')
    )
    order_index = models.PositiveIntegerField(
        verbose_name=_('order index')
    )
    video = models.URLField(
        blank=True,
        verbose_name=_('video')
    )
    video_image = models.URLField(
        blank=True,
        verbose_name=_('video image')
    )
    attached_product = models.OneToOneField(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='section',
        verbose_name=_('product')
    )
    attached_section = models.OneToOneField(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='section',
        verbose_name=_('section')
    )
    cover_primary = models.ForeignKey(
        SectionImage,
        blank=True,
        null=True,
        related_name='primary_sections',
        on_delete=models.SET_NULL,
        verbose_name = _('primary cover')
    )
    cover_secondary = models.ForeignKey(
        SectionImage,
        blank=True,
        null=True,
        related_name='secondary_sections',
        on_delete=models.SET_NULL,
        verbose_name = _('secondary cover')
    )

    objects = SectionModelManager()

    def video_image_tag(self):
        return super(Section, self).image_tag(image_url=self.video_image)
    video_image_tag.short_description = _('Video image')

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Feature(Element): 
    section = models.ForeignKey(
        Section, 
        null=True, 
        related_name='features', 
        on_delete=models.SET_NULL
    )
    prefix = models.TextField(
        blank=True, 
        verbose_name=_('prefix text')
    )
    subtitle = models.CharField(
        blank=True, 
        max_length=50, 
        verbose_name=_('subtitle')
    )

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')


class SearchSuggestion(Element):

    class Meta:
        verbose_name = _('search suggestion')
        verbose_name_plural = _('search suggestions')


class LandingPageQuerySet(FeaturedModelQuerySet):
    
    pass


class LandingPage(Element, FeaturedModel, TimeStampedModel):
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('slug'),
    )
    enable_pinned_content = models.BooleanField(
        default=True,
        verbose_name=_('enable pinned content'),
    )
    enable_signin = models.BooleanField(
        default=True,
        verbose_name=_('enable sign in section'),
    )
    sections = models.ManyToManyField(
        Section,
        related_name = 'landing_pages', 
        blank = True, 
        verbose_name = _('sections'),
    )
    THEME_CHOICES = (
        ('landing/landing_quick.html', 'quick classic'),
        ('landing/landing_quick_onepage.html', 'quick onepage'),
        ('landing/landing_custom_onepage.html', 'custom onepage')

    )
    THEME_DEFAULT = 'landing/landing_quick.html'
    theme = models.CharField(
        max_length=50,
        choices=THEME_CHOICES, 
        default=THEME_DEFAULT, 
        verbose_name=_('theme')
    )

    objects = LandingPageQuerySet.as_manager()

    def __str__(self):
        return '%s' % (self.title)

    def get_absolute_url(self):
        return reverse('landing:page_detail', args=[str(self.slug)])

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')


