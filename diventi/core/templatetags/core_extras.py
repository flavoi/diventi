from django import template

register = template.Library()


@register.filter()
def to_float(value):
    if value:
        return float(value)
    else:
        return 0