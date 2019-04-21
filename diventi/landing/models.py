from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.html import mark_safe

from cuser.middleware import CuserMiddleware

from diventi.core.models import Element, DiventiImageModel, FeaturedModel
from diventi.accounts.models import DiventiUser
from diventi.products.models import Product
from diventi.feedbacks.models import Survey
from diventi.blog.models import Article


class Section(DiventiImageModel, FeaturedModel):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    abstract = models.TextField(blank=True, verbose_name=_('abstract'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    TEMPLATE_CHOICES = (
        ('section_centered.html', _('standard centered section')),
        ('section_left.html', _('standard left section')),
        ('section_right.html', _('standard right section')),
    )
    template = models.CharField(choices=TEMPLATE_CHOICES, max_length=50, verbose_name=_('standard template'))
    FEATURED_TEMPLATE_CHOICES = (
        ('header_left.html', _('standard left header')),
        ('header_centered.html', _('standard centered header')),
    )
    featured_template = models.CharField(choices=FEATURED_TEMPLATE_CHOICES, max_length=50, verbose_name=_('featured template'))
    products = models.ManyToManyField(Product, related_name='products', blank=True, verbose_name=_('products'))
    users = models.ManyToManyField(DiventiUser, related_name='users', blank=True, verbose_name=_('users'))
    section_survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('survey'))
    section_article = models.ForeignKey(Article, related_name='article', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('article'))

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    def get_features(self):
        return mark_safe("<br>".join([s.title for s in self.section_features.all()]))
    get_features.short_description = _('Features')

    def get_products(self):
        return mark_safe("<br>".join([s.title for s in self.products.all()]))
    get_products.short_description = _('Products')

    def get_users(self):
        return mark_safe("<br>".join([s.get_full_name() for s in self.users.all()]))
    get_users.short_description = _('Users')


    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Feature(Element):    
    section = models.ForeignKey(Section, null=True, related_name='section_features', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
        
