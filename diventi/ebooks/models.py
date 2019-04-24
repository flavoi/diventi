from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from diventi.products.models import Product
from diventi.core.models import Element, TimeStampedModel, PublishableModel


class Section(Element, TimeStampedModel):
    """ A section of prodcut's content. """
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))
    content = RichTextField(verbose_name=_('content'))
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('product'))

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')
