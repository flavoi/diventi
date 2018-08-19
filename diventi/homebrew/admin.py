from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline
from diventi.core.admin import DiventiTranslationAdmin

from .models import Paper, Section, Watermark


class SectionInline(TranslationStackedInline):
    model = Section
    fields = ('order_id', 'title', 'content', 'section_type')
    extra = 0


class WatermarkInline(TranslationStackedInline):
    model = Watermark
    fields = ('title', 'pages', 'scale', 'xpos', 'ypos', 'figurename')
    extra = 0


class PaperAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'description']
    readonly_fields = ['created', 'modified']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [        
        SectionInline,
        WatermarkInline,
    ]

admin.site.register(Paper, PaperAdmin)
