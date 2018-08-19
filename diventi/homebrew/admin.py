from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline
from diventi.core.admin import DiventiTranslationAdmin

from .models import Paper, Section


class SectionInline(TranslationStackedInline):
    model = Section
    fields = ('order_id', 'title', 'content', 'section_type')
    extra = 0


class PaperAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'description']
    readonly_fields = ['created', 'modified']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [        
        SectionInline,
    ]

admin.site.register(Paper, PaperAdmin)
