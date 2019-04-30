from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished

from .models import Book, Chapter, Section


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


class BookAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'created', 'modified', 'published', 'publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published',)
        }),
        (_('Editing'), {
            'fields': ('title', 'short_title', 'category', 'slug', 'created', 'modified', 'publication_date'),
        }),
    )
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_published, make_unpublished]


class ChapterAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'chapter_book', 'created', 'modified',]
    fieldsets = (
        (_('Pubblication'), {
            'fields': ('chapter_book',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'slug', 'created', 'modified'),
        }),
    )
    readonly_fields = ['created', 'modified',]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order_index']
    actions = [make_published, make_unpublished]
    inlines = [SectionInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)