from django import template
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_comments.templatetags.comments import CommentListNode
from mptt.utils import get_cached_trees
from mptt.templatetags.mptt_tags import RecurseTreeNode

register = template.Library()


class DiventiCommentListNode(CommentListNode):
    """Fetches a list of comments customized for Diventi context."""

    def get_context_value_from_queryset(self, context, qs):
        return qs


class DateOrderedRecurseTreeNode(RecurseTreeNode):
    """Insert a list of comments ordered by submit date into the context."""

    def render(self, context):
        queryset = self.queryset_var.resolve(context)
        roots = get_cached_trees(queryset)
        roots.sort(key=lambda node: node.submit_date, reverse=True)
        bits = [super(DateOrderedRecurseTreeNode, self)._render_node(context, node) for node in roots]
        return ''.join(bits)


class PromotionOrderedRecurseTreeNode(RecurseTreeNode):
    """Insert a list of comments ordered by the number of promotions into the context."""

    def render(self, context):
        queryset = self.queryset_var.resolve(context)
        queryset = queryset.annotate(promotions_count=Count('promotions'))      
        roots = get_cached_trees(queryset)
        roots.sort(key=lambda node: node.promotions_count, reverse=True)
        bits = [super(PromotionOrderedRecurseTreeNode, self)._render_node(context, node) for node in roots]
        return ''.join(bits)


@register.tag
def get_comment_list(parser, token):
    return DiventiCommentListNode.handle_token(parser, token)

@register.tag
def dateorderedcursetree(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a queryset') % bits[0])

    queryset_var = template.Variable(bits[1])
    template_nodes = parser.parse(('endrecursetree',))
    parser.delete_first_token()

    return DateOrderedRecurseTreeNode(template_nodes, queryset_var)

@register.tag
def promotionorderedcursetree(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a queryset') % bits[0])

    queryset_var = template.Variable(bits[1])
    template_nodes = parser.parse(('endrecursetree',))
    parser.delete_first_token()

    return PromotionOrderedRecurseTreeNode(template_nodes, queryset_var)