from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished

from .models import Book, Chapter, Section, UniversalSection


class UniversalSectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'get_universal_chapter',]
    fields = ['title', 'order_index', 'content',]
    ordering = ['order_index']


class SectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'internal_order_index', 'chapter',]
    fieldsets = (
        (_('Universal content'), {
            'fields': ('universal_section',)
        }),
        (_('Table of contents'), {
            'fields': ('chapter',)
        }),
        (_('Editing'), {
            'fields': ('title', 'internal_order_index', 'order_index', 'content', 'slug',),
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['internal_order_index', ]
    readonly_fields = ['internal_order_index',
    ]


class SectionInline(TranslationStackedInline):
    model = Section
    fieldsets = (
        (_('Universal content'), {
            'fields': ('universal_section',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'content', 'slug',),
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order_index']
    extra = 0


class BookAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'get_product_image', 'get_product_category', 'created', 'modified', 'published', 'publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'book_product')
        }),
        (_('Editing'), {
            'fields': ('title', 'short_title', 'slug', 'created', 'modified', 'publication_date'),
        }),
    )
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_published, make_unpublished]
    search_fields = ['title']
    save_as = True


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
    list_filter = ['chapter_book',]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order_index']
    inlines = [SectionInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(UniversalSection, UniversalSectionAdmin)