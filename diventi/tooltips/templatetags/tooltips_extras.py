from django import template
from django.utils.html import strip_tags, mark_safe

from diventi.tooltips.models import Tooltip

register = template.Library()

@register.filter(name='tooltip')
def tooltip(value, section_pk):
    """
        Fetch the available tooltips and inject a short
        description on top of the keywords. 
        It does not inject any content to the source section.
        It replaces the first keyword occurence only.
    """
    tooltips = Tooltip.objects.all().prefetch()
    for tooltip in tooltips:
        section = tooltip.section
        if section_pk != section.pk:
            value = value.replace(
                tooltip.title,
                mark_safe(
                    '<button type="button" data-wenk="📰 {tooltip_content}" class="wenk-length--large">\
                        {tooltip_title}\
                    </button>'.format(
                        tooltip_id=tooltip.pk,
                        tooltip_content=strip_tags(section.get_converted_description()),
                        tooltip_title=tooltip.title,
                    )
                ),
                1
            )
    return value