from django.db import models
from django_comments.abstracts import CommentAbstractModel

from diventi.core.models import PromotableModel


class DiventiComment(CommentAbstractModel, PromotableModel):
    pass