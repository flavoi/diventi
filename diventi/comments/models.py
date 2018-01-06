from django.db import models
from django.utils.translation import gettext_lazy as _

from django_comments.abstracts import CommentAbstractModel
from mptt.models import MPTTModel, TreeForeignKey

from diventi.core.models import PromotableModel


class DiventiComment(MPTTModel, CommentAbstractModel, PromotableModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('parent'))

    class MPTTMeta:
        order_insertion_by = ['submit_date']

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return self.comment
