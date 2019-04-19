from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.html import mark_safe

from cuser.middleware import CuserMiddleware

from diventi.core.models import Element, DiventiImageModel, FeaturedModel
from diventi.accounts.models import DiventiUser
from diventi.products.models import Product
from diventi.feedbacks.models import Survey


class PresentationManager(models.Manager):

    def active(self):
        try:
            active_presentation = self.prefetch_related('profile_features')            
            active_presentation = active_presentation.get(active=True)
        except Presentation.DoesNotExist:
            msg = _("There is no active landing page.")
            raise Presentation.DoesNotExist(msg)
        except Presentation.MultipleObjectsReturned:
            msg = _("There must be only one landing page at a time. Please fix!")
            raise Presentation.MultipleObjectsReturned(msg)
        return active_presentation


class Presentation(DiventiImageModel):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    abstract = models.TextField(blank=True, verbose_name=_('abstract'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    projects_description = models.TextField(blank=True, verbose_name=_('projects description'))
    featured_link = models.CharField(blank=True, max_length=150, verbose_name=_('featured link'))
    featured_label = models.CharField(blank=True, max_length=50, verbose_name=_('featured label'))
    TEMPLATE_CHOICES = (
        ('standard_left_header.html', _('standard left header')),
        ('survey_centered_header.html', _('standard centered header')),
    )
    template = models.CharField(choices=TEMPLATE_CHOICES, max_length=50, verbose_name=_('template'))
    active = models.BooleanField(default=False, verbose_name=_('active'))
    
    objects = PresentationManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('presentation')
        verbose_name_plural = _('presentations')


class Section(DiventiImageModel, FeaturedModel):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    abstract = models.TextField(blank=True, verbose_name=_('abstract'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    TEMPLATE_CHOICES = (
        ('standard_centered_section.html', _('standard centered section')),
    )
    template = models.CharField(choices=TEMPLATE_CHOICES, max_length=50, verbose_name=_('standard template'))
    FEATURED_TEMPLATE_CHOICES = (
        ('standard_left_header.html', _('standard left header')),
        ('survey_centered_header.html', _('standard centered header')),
    )
    featured_template = models.CharField(choices=FEATURED_TEMPLATE_CHOICES, max_length=50, verbose_name=_('featured template'))
    products = models.ManyToManyField(Product, related_name='products', blank=True, verbose_name=_('products'))
    users = models.ManyToManyField(DiventiUser, related_name='users', blank=True, verbose_name=_('users'))
    section_survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('survey'))

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
        
