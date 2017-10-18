from django import template
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_comments.templatetags.comments import CommentListNode

register = template.Library()


class PaginatedListNote:
    
    def get_paginated_qs(self, context, qs, pages):
        paginator = Paginator(qs, pages)
        page = context['request'].GET.get('page')
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            qs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            qs = paginator.page(paginator.num_pages)
        return qs


class DateOrderedCommentListNode(CommentListNode):
    """Insert a list of comments ordered by submit date into the context."""

    def get_context_value_from_queryset(self, context, qs):
        qs = qs.order_by('-submit_date')
        return qs


class PromotionOrderedCommentListNode(CommentListNode, PaginatedListNote):
    """Insert a list of comments ordered by the number of promotions into the context."""

    def get_context_value_from_queryset(self, context, qs):
        qs = qs.annotate(promotions_count=Count('promotions'))
        qs = qs.order_by('-promotions_count')
        qs = self.get_paginated_qs(context, qs, 3)
        return qs


@register.tag
def get_comment_list_by_date(parser, token):
    return DateOrderedCommentListNode.handle_token(parser, token)


@register.tag
def get_comment_list_by_promotions(parser, token):
    return PromotionOrderedCommentListNode.handle_token(parser, token)