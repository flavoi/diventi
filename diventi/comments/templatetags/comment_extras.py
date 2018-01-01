from django import template
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_comments.templatetags.comments import CommentListNode

register = template.Library()


class DateOrderedCommentListNode(CommentListNode):
    """Insert a list of comments ordered by submit date into the context."""

    def get_context_value_from_queryset(self, context, qs):
        qs = qs.order_by('tree_id', 'level', '-submit_date')
        return qs


class PromotionOrderedCommentListNode(CommentListNode):
    """Insert a list of comments ordered by the number of promotions into the context."""

    def get_context_value_from_queryset(self, context, qs):
        qs = qs.annotate(promotions_count=Count('promotions'))
        qs = qs.order_by('tree_id', 'level', '-promotions_count')
        return qs


@register.tag
def get_comment_list_by_date(parser, token):
    return DateOrderedCommentListNode.handle_token(parser, token)

@register.tag
def get_comment_list_by_promotions(parser, token):
    return PromotionOrderedCommentListNode.handle_token(parser, token)