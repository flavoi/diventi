from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline
from diventi.core.admin import DiventiTranslationAdmin

from .models import Paper, Section, Watermark, DiceTable, DiceTableRow


class SectionInline(TranslationStackedInline):
    model = Section
    fields = ('order_id', 'title', 'content', 'theme', 'table', 'section_type', 'new_page', 'title_page')
    extra = 0
    ordering = ["order_id"]


class WatermarkInline(TranslationStackedInline):
    model = Watermark
    fields = ('title', 'pages', 'scale', 'xpos', 'ypos', 'figurename')
    extra = 0
    ordering = ["pages"]


class PaperAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'description']
    readonly_fields = ['created', 'modified']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [        
        SectionInline,
        WatermarkInline,
    ]


class DiceTableRowInline(TranslationStackedInline):
    model = DiceTableRow
    fields = ('description',)
    extra = 0


class DiceTableAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'dice']
    inlines = [
        DiceTableRowInline,
    ]


admin.site.register(Paper, PaperAdmin)
admin.site.register(DiceTable, DiceTableAdmin)
