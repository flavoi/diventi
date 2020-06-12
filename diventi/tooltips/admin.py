from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin
from diventi.ebooks.forms import SectionProductForm

from .models import (
    Tooltip,
    TooltipGroup,
)

from .forms import TooltipForm


class TooltipAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'group', 'product', 'section']
    form = TooltipForm
    list_filter = ['group',]


class TooltipGroupAdmin(DiventiTranslationAdmin):
    list_display = ['title',]
    fields = ('title',)


admin.site.register(Tooltip, TooltipAdmin)
admin.site.register(TooltipGroup, TooltipGroupAdmin)