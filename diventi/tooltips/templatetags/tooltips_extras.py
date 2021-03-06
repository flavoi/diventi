from django import template
from django.utils.html import strip_tags, mark_safe

from diventi.ebooks.models import (
    Book,
    Section,
)
from diventi.tooltips.models import (
    Tooltip,
    TooltipGroup,
)

register = template.Library()


@register.filter(name='tooltip')
def tooltip(value, section_pk):
    """
        This method fetches the available tooltips and injects a short
        description on top of the keywords. 
        It does not injects any content to the source section.
        It replaces the first keyword occurence only.
    """
    try:
        section = Section.objects.get(pk=section_pk)
        book = section.chapter.chapter_book
        tooltip_group = TooltipGroup.objects.get(books=book)
        tooltips = tooltip_group.tooltips.all().prefetch()
        for tooltip in tooltips:
            section = tooltip.section
            if section_pk != section.pk:
                value = value.replace(
                    tooltip.title,
                    mark_safe(
                        '<a href="#" data-micromodal-trigger="modal-{tooltip_pk}">\
                         <i class="fad fa-info-circle"></i> {tooltip_title}</a>'.format(
                            tooltip_pk=tooltip.pk,
                            tooltip_title=tooltip.title,
                        )
                    ),
                    1
                )
    except TooltipGroup.DoesNotExist:
        pass
    return value
