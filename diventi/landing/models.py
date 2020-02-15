from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.html import mark_safe

from cuser.middleware import CuserMiddleware

from diventi.core.models import Element, DiventiImageModel, FeaturedModel, FeaturedModelManager
from diventi.accounts.models import DiventiUser
from diventi.products.models import Product
from diventi.feedbacks.models import Survey
from diventi.blog.models import Article


class SectionModelManager(FeaturedModelManager):

    # Get the non featured sections that appear on the landing page
    # Pre-loads related objects to speed up the templates
    def not_featured(self):
        sections = super(SectionModelManager, self).not_featured()
        sections = sections.prefetch_related('users')
        sections = sections.prefetch_related('products').prefetch_related('products__chapters')
        sections = sections.select_related('section_survey')
        sections = sections.prefetch_related('articles')
        sections = sections.order_by('order_index')
        return sections


class Section(DiventiImageModel, FeaturedModel):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    TEMPLATE_CHOICES = (
        ('standard_section.html', _('standard section')),
        ('cards_section.html', _('cards section')),
    )
    template = models.CharField(choices=TEMPLATE_CHOICES, max_length=50, verbose_name=_('standard template'))
    FEATURED_TEMPLATE_CHOICES = (
        ('standard_header.html', _('standard header')),
        ('search_header.html', _('search header')),
    )
    featured_template = models.CharField(choices=FEATURED_TEMPLATE_CHOICES, max_length=50, verbose_name=_('featured template'))
    dark_mode = models.BooleanField(verbose_name=_('dark mode'))
    ALIGNMENT_CHOICES = (
        ('left', _('left')),
        ('centered', _('centered')),
        ('right', _('right')),
    )
    alignment = models.CharField(choices=ALIGNMENT_CHOICES, max_length=50, verbose_name=_('alignment'))
    products = models.ManyToManyField(Product, related_name='products', blank=True, verbose_name=_('products'))
    users = models.ManyToManyField(DiventiUser, related_name='users', blank=True, verbose_name=_('users'))
    section_survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('survey'))
    articles = models.ManyToManyField(Article, related_name='articles', blank=True, verbose_name=_('articles'))

    objects = SectionModelManager()

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    def get_features(self):
        return mark_safe("<br>".join([obj.title for obj in self.section_features.all()]))
    get_features.short_description = _('Features')

    def get_products(self):
        return mark_safe("<br>".join([obj.title for obj in self.products.all()]))
    get_products.short_description = _('Products')

    def get_users(self):
        return mark_safe("<br>".join([obj.get_full_name() for obj in self.users.all()]))
    get_users.short_description = _('Users')

    def get_articles(self):
        return mark_safe("<br>".join([obj.title for obj in self.articles.all()]))
    get_articles.short_description = _('Articles')

    def get_alignment_classes(self):     
        if self.alignment == 'left':
            alignment_classes = 'mr-auto text-left'
        elif self.alignment == 'centered':
            alignment_classes = 'ml-auto mr-auto text-center'
        elif self.alignment == 'right':
            alignment_classes = 'ml-auto text-right'
        else:
            alignment_classes = ''   
        return alignment_classes

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Feature(Element):    
    section = models.ForeignKey(Section, null=True, related_name='section_features', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
        
