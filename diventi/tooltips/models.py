from django.db import models
from django.utils.translation import gettext_lazy as _

from diventi.core.models import (
    Element,
)
from diventi.ebooks.models import (
    Book,
    Section,
)
from diventi.products.models import (
    Product,
)


class TooltipGroup(Element):
    """
        A tooltip group is a collection of tooltips centered around
        a certain application.
    """
    books = models.ManyToManyField(
        Book,
        blank=True,
        verbose_name=_('book')
    )

    class Meta:
        verbose_name = _('tooltip group')
        verbose_name_plural = _('tooltip groups')


class TooltipQuerySet(models.QuerySet):

    # Select tooltip's related objects
    def prefetch(self):
        tooltips = self.select_related('section')
        tooltips = tooltips.select_related('product')
        tooltips = tooltips.select_related('group')
        return tooltips


class Tooltip(Element):
    group = models.ForeignKey(
        TooltipGroup, 
        null=True, 
        blank=True,
        related_name='tooltips', 
        on_delete=models.SET_NULL,
        verbose_name=_('group'),
    )
    section = models.ForeignKey(
        Section,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='tooltips',
        verbose_name=_('section'),
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tooltips',
        verbose_name=_('product'),
    )


    objects = TooltipQuerySet.as_manager()
    
    class Meta:
        verbose_name = _('Tooltip')
        verbose_name_plural = _('Tooltips')