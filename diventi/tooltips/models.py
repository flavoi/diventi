from django.db import models
from django.utils.translation import gettext_lazy as _

from diventi.core.models import (
    Element,
)
from diventi.ebooks.models import (
    Section,
)
from diventi.products.models import (
    Product,
)

class Keyword(Element):

    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')


class TooltipQuerySet(models.QuerySet):

    # Select adventure's related objects
    def prefetch(self):
        tooltips = self.select_related('section')
        tooltips = tooltips.select_related('product')
        return tooltips


class Tooltip(Element):
    keywords = models.ManyToManyField(
        Keyword,
        blank=True,
        verbose_name=_('keyword')
    )
    section = models.ForeignKey(
        Section,
        blank=False,
        null=True,
        verbose_name=_('section'),
        on_delete=models.SET_NULL,
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tooltip',
        verbose_name=_('product'),
    )

    objects = TooltipQuerySet.as_manager()
    
    class Meta:
        verbose_name = _('Tooltip')
        verbose_name_plural = _('Tooltips')