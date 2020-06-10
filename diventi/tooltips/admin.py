from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin
from diventi.ebooks.forms import SectionProductForm

from .models import (
    Keyword,
    Tooltip
)

from .forms import TooltipForm


class KeywordAdmin(DiventiTranslationAdmin):
    list_display = ['title',]
    fields = ('title',)


class TooltipAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'product', 'section']
    form = TooltipForm


admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tooltip, TooltipAdmin)