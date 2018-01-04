from django.db import models

from django_comments.abstracts import CommentAbstractModel
from mptt.models import MPTTModel, TreeForeignKey

from diventi.core.models import PromotableModel


class DiventiComment(MPTTModel, CommentAbstractModel, PromotableModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['submit_date']

    def __str__(self):
        return self.comment
