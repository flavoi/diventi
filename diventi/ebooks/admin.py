from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished

from .models import Chapter, Section


class SectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'chapter',]
    fields = ('chapter', 'title', 'order_index', 'content', 'slug')
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['chapter__order_index', 'order_index']


class SectionInline(TranslationStackedInline):
    model = Section
    fields = ('title', 'order_index', 'content', 'slug')
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order_index']
    extra = 0


class ChapterAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index']
    fieldsets = (
        (_('Management'), {
            'fields': ('published',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'slug', 'publication_date'),
        }),
    )
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order_index']
    actions = [make_published, make_unpublished]
    inlines = [SectionInline]


admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)