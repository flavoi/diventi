from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from modeltranslation.admin import TranslationStackedInline, TranslationTabularInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished

from .models import (
    Book, 
    Chapter, 
    Section, 
    UniversalSection, 
    Part, 
    ReplacementRule,
    SectionAspect,
    Secret,
)

from .forms import SectionForm

def duplicate_section(modeladmin, request, queryset):
    for section in queryset:
        section.id = None
        section.chapter = None
        section.save()
duplicate_section.short_description = _("Duplicate selected section")


class UniversalSectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'get_universal_chapter',]
    fields = ['title', 'order_index', 'description', 'content',]
    search_fields = ['title']
    ordering = ['order_index']


class SectionAspectInline(TranslationStackedInline):
    model = SectionAspect
    fields = ('aspect_type', 'title', 'icon')
    extra = 0


class SecretInline(TranslationStackedInline):
    model = Secret
    fields = ('secret_type', 'title', 'description', 'icon', 'requires_skill_check')
    extra = 0


class SectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'chapter', 'image_tag', 'get_rules']
    form = SectionForm
    fieldsets = (
        (_('Universal content'), {
            'fields': ('universal_section', 'rules')
        }),
        (_('Table of contents'), {
            'fields': ('book', 'chapter', 'bookmark')
        }),
        (_('Layout'), {
            'fields': ('image', 'text_alignment',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'description', 'content', 'situation', 'slug'),
        }),
    )
    inlines = [
        SectionAspectInline,
        SecretInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['chapter__order_index', 'order_index']
    search_fields = ['chapter__chapter_book__title', 'title']
    autocomplete_fields = ['universal_section', 'chapter']
    list_filter = ['chapter__chapter_book',]
    preserve_filters = True
    actions = [duplicate_section,]
    

class PartAdmin(DiventiTranslationAdmin):
    list_display = ['title', ]
    fields = ['title',]


class ReplacementRuleAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'initial_string', 'result_string']
    fields = ['title', 'initial_string', 'result_string']


class BookAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'published', 'continuous_update', 'legacy_paper_id', 'paper_id', 'content_file_url', 'image_tag', 'get_logo_image', 'get_product_category', 'get_hitcounts', 'created', 'modified', 'publication_date']
    fieldsets = (        
        (_('Management'), {
            'fields': ('published', 'book_product', 'continuous_update'),
        }),
        (_('Content'), {
            'fields': ('paper_id', 'legacy_paper_id', 'content_file_url', 'image'),
        }),        
        (_('Layout'), {
            'fields': ('logo',),
        }),
        (_('Editing'), {
            'fields': ('title', 'description', 'summary', 'slug', 'created', 'modified', 'publication_date'),
        }),
    )
    readonly_fields = ['created', 'modified', 'publication_date']
    list_filter = ('book_product__category', 'continuous_update')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title']
    actions = [make_published, make_unpublished]
    save_as = True


class ChapterAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'order_index', 'chapter_book', 'updated', 'new', 'part', 'created', 'modified',]
    fieldsets = (
        (_('Pubblication'), {
            'fields': ('chapter_book', 'updated', 'new')
        }),
        (_('Layout'), {
            'fields': ('image',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'part', 'description', 'slug', 'created', 'modified'),
        }),
    )
    readonly_fields = ['created', 'modified',]
    list_filter = ['chapter_book',]
    preserve_filters = True
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order_index']
    search_fields = ['title',]


class SectionCategoryadmin(DiventiTranslationAdmin):
    list_display = ['title', 'default',]


admin.site.register(Book, BookAdmin)
