from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline
from diventi.core.admin import DiventiTranslationAdmin, duplicate

from .models import Paper, Section, Watermark, DiceTable, DiceTableRow, Itemize, ItemizeItem, CharacterBlock, CharacterItem, Card


class SectionInline(TranslationStackedInline):
    model = Section
    fields = ('order_id', 'title', 'content', 'theme', 'table', '_list', 'character', '_card', '_illustration', 'section_type', 'new_page', 'title_page')
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
    actions = [duplicate,]


class DiceTableRowInline(TranslationStackedInline):
    model = DiceTableRow
    fields = ('face', 'description')
    extra = 0
    ordering = ["face"]


class DiceTableAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'dice']
    inlines = [
        DiceTableRowInline,
    ]


class ItemizeItemInline(TranslationStackedInline):
    model = ItemizeItem
    fields = ('description',)
    extra = 0


class ItemizeAdmin(DiventiTranslationAdmin):
    list_display = ['title',]
    inlines = [
        ItemizeItemInline,
    ]


class CharacterItemInline(TranslationStackedInline):
    model = CharacterItem
    fields = ('title', 'description',)
    extra = 0


class CharacterBlockAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'description']
    inlines = [
        CharacterItemInline,
    ]


admin.site.register(Paper, PaperAdmin)
admin.site.register(DiceTable, DiceTableAdmin)
admin.site.register(Itemize, ItemizeAdmin)
admin.site.register(CharacterBlock, CharacterBlockAdmin)
admin.site.register(Card)
