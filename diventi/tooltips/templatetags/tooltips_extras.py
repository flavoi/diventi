from django import template
from django.utils.html import strip_tags, mark_safe

from diventi.tooltips.models import Tooltip

register = template.Library()

# Da completare: 
# Aggiungere stili tooltip alle pagine ebook
# Aggiungere ricerca maiuscole/minuscole
# Escludere dalla ricerca i contenuti della sezione tooltip
# Raffinare il contenuto del tooltip
@register.filter(name='tooltip')
def tooltip(value, section_pk):
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
                )
            )
    return value