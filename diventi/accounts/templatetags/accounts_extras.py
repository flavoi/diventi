import re

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.template.defaulttags import register
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

readmore_showscript = ''.join([
"this.parentNode.style.display='none';",
"this.parentNode.parentNode.getElementsByClassName('more')[0].style.display='inline';",
"return false;",
]);

@register.filter
def readmore(txt, showwords=15):
    global readmore_showscript
    words = re.split(r' ', escape(txt))
    if len(words) <= showwords:
        return txt
    # wrap the more part
    words.insert(showwords, '<span class="more" style="display:none;">')
    words.append('</span>')
    # insert the readmore part
    words.insert(showwords, '<span class="readmore">... <a class="text-warning" href="#" onclick="')
    words.insert(showwords+1, readmore_showscript)
    words.insert(showwords+2, '">read more</a>')
    words.insert(showwords+3, '</span>')
    return mark_safe(' '.join(words))

readmore.is_safe = True