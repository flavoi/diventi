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
    FeaturedModelManager, 
    SectionModel,
    PublishableModel,
    TimeStampedModel,
    PromotableModel,
)

from diventi.accounts.models import DiventiUser
from diventi.products.models import Product
from diventi.feedbacks.models import Survey
from diventi.blog.models import Article


class SectionModelManager(FeaturedModelManager):

    # Get the non featured sections that appear on the landing page
    def not_featured(self):
        sections = super(SectionModelManager, self).not_featured()
        sections = sections.order_by('order_index')
        return sections


class Section(DiventiImageModel, FeaturedModel, SectionModel):
    prefix = models.TextField(blank=True, verbose_name=_('prefix text'))
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
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




