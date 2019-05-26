from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from modeltranslation.admin import TranslationStackedInline, TranslationTabularInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished

from .models import Book, Chapter, Section, UniversalSection


class UniversalSectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'get_universal_chapter',]
    fields = ['title', 'order_index', 'content',]
    ordering = ['order_index']


class FilteredSectionAdminMixin(admin.options.BaseModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super(FilteredSectionAdminMixin, self).get_form(request, obj, **kwargs)
        """
            Adjust the section queryset to cope with the following requirement:
            A universal section should be used only one per book.            
        """
        if obj is not None and obj.chapter is not None:
            book = obj.chapter.chapter_book
            sections = Section.objects.filter(chapter__chapter_book=book)
            q = UniversalSection.objects.all().exclude(sections__in=sections)
            if obj.universal_section is not None: # Don't exclude the current universal section
                universal_section = UniversalSection.objects.filter(pk=obj.universal_section.pk)
                q = q | universal_section  
            form.base_fields['universal_section'].queryset = q
        return form


class SectionAdmin(FilteredSectionAdminMixin, DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'chapter', 'super_title', 'color_tag', 'image_tag', 'icon_tag']
    fieldsets = (
        (_('Universal content'), {
            'fields': ('universal_section',)
        }),
        (_('Table of contents'), {
            'fields': ('chapter',)
        }),
        (_('Layout'), {
            'fields': ('col_lg', 'col_md', 'image', 'text_alignment', 'color', 'icon', 'super_title',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'description', 'content',),
        }),
    )
    ordering = ['chapter__order_index', 'order_index']


class SectionInline(FilteredSectionAdminMixin, TranslationStackedInline):
    model = Section
    fields = ('universal_section', 'title', 'order_index', 'content',)
    ordering = ['order_index']
    extra = 0


class BookAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'get_product_image', 'get_product_category', 'created', 'modified', 'published', 'publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'book_product')
        }),
        (_('Layout'), {
            'fields': ('col_lg', 'col_md',)
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