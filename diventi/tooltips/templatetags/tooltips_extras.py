from django import template
from django.utils.html import strip_tags, mark_safe

from diventi.tooltips.models import Tooltip

register = template.Library()

# Da completare: 
# Aggiungere stili tooltip alle pagine ebook
# Aggiungere ricerca maiuscole/minuscole
# Escludere dalla ricerca i contenuti della sezione tooltip
@register.filter(name='tooltip')
def tooltip(value):
    tooltips = Tooltip.objects.all()
    for tooltip in tooltips:
        print(tooltip.title)
        value = value.replace(
            tooltip.title,
            mark_safe(
                '<button type="button" class="btn btn-secondary" data-container="body"\
                 data-toggle="popover" data-placement="top" data-content="Vivamus sagittis\
                 lacus vel augue laoreet rutrum faucibus.">{}</button>'.format(tooltip.title)
            )
        )
    return value