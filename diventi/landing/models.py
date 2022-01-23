from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.html import mark_safe
from django.urls import reverse
from django.db.models import Prefetch

from cuser.middleware import CuserMiddleware
from ckeditor.fields import RichTextField

from diventi.core.models import (
    Element, 
    DiventiImageModel, 
    FeaturedModel, 
    FeaturedModelQuerySet,
    FeaturedModelManager,
    SectionModel,
    PublishableModel,
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


class AboutArticle(TimeStampedModel, PublishableModel, Element):
    content = RichTextField(verbose_name=_('content'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))

    def get_absolute_url(self):
        return reverse('landing:about', args=[str(self.slug,)])

    class Meta:
        verbose_name = _('about article')
        verbose_name_plural = _('about article')


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
        sections = self.select_related('about_article')
        sections = sections.select_related('product_category')
        sections = sections.select_related('article_category')
        sections = section.prefetch_related('features')
        return sections

    # Get the not featured object that can be selected to appear on the landing page
    def not_featured(self):
        not_featured_models = self.published().filter(featured=False)
        return not_featured_models


class SectionModelManager(FeaturedModelManager):

    def get_queryset(self):
        return SectionModelQuerySet(self.model, using=self._db)

    def not_featured(self):
        return self.get_queryset().not_featured()


class Section(DiventiImageModel, FeaturedModel, SectionModel):
    prefix = models.TextField(blank=True, verbose_name=_('prefix text'))
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    button_label = models.CharField(blank=True, max_length=50, verbose_name=_('button label'))
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    attachment_label = models.CharField(blank=True, max_length=50, verbose_name=_('attachment label'))
    about_article = models.ForeignKey(
        AboutArticle,
        blank = True,
        null = True,
        related_name='sections',
        on_delete=models.SET_NULL,
        verbose_name=_('about article'),
    )
    product_category = models.ForeignKey(
        ProductCategory,
        blank = True,
        null = True,
        related_name='sections',
        on_delete=models.SET_NULL,
        verbose_name=_('product category'),
    )
    article_category = models.ForeignKey(
        ArticleCategory,
        blank = True,
        null = True,
        related_name='sections',
        on_delete=models.SET_NULL,
        verbose_name=_('article category'),
    )
    video = models.URLField(
        blank=True,
        verbose_name=_('video')
    )


    objects = SectionModelManager()

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Feature(Element): 
    section = models.ForeignKey(Section, null=True, related_name='features', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')


class SearchSuggestion(Element):

    class Meta:
        verbose_name = _('search suggestion')
        verbose_name_plural = _('search suggestions')




