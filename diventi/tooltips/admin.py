from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import (
    TranslationStackedInline,
    TranslationTabularInline,
)

from diventi.core.admin import DiventiTranslationAdmin
from diventi.ebooks.forms import SectionProductForm

from .models import (
    Tooltip,
    TooltipGroup,
)

from .forms import TooltipForm


class TooltipAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'group', 'paper_mention_link']
    form = TooltipForm
    list_filter = ['group',]


class TooltipInline(TranslationTabularInline):
    model = Tooltip
    form = TooltipForm
    extra = 3


class TooltipGroupAdmin(DiventiTranslationAdmin):
    list_display = ['title',]
    fields = ('title', 'books')
    filter_horizontal = ('books',)
    inlines = [
        TooltipInline,
    ]

admin.site.register(Tooltip, TooltipAdmin)
admin.site.register(TooltipGroup, TooltipGroupAdmin)