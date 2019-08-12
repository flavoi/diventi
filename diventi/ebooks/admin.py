from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from modeltranslation.admin import TranslationStackedInline, TranslationTabularInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished

from .models import Book, Chapter, Section, UniversalSection, Attachment

def duplicate_section(modeladmin, request, queryset):
    for section in queryset:
        section.id = None
        section.chapter = None
        section.save()
duplicate_section.short_description = _("Duplicate selected section")

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


class AttachmentInline(TranslationStackedInline):
    model = Attachment
    fields = ['title', 'content']
    extra = 0


class AttachmentAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'section']
    fields = ['title', 'content', 'section']


class SectionAdmin(FilteredSectionAdminMixin, DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'chapter', 'color_tag', 'image_tag', 'icon_tag', 'get_attachments']
    fieldsets = (
        (_('Universal content'), {
            'fields': ('universal_section',)
        }),
        (_('Table of contents'), {
            'fields': ('chapter', 'bookmark')
        }),
        (_('Layout'), {
            'fields': ('col_lg', 'col_md', 'image', 'text_alignment', 'color',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'description', 'content', 'slug'),
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['chapter__order_index', 'order_index']
    search_fields = ['chapter__chapter_book__title', 'title']
    list_filter = ['chapter__chapter_book',]
    inlines = [AttachmentInline]
    actions = [duplicate_section,]


class SectionInline(TranslationStackedInline):
    model = Section
    fieldsets = (
        (_('Universal content'), {
            'fields': ('universal_section',)
        }),
        (_('Table of contents'), {
            'fields': ('bookmark',)
        }),
        (_('Layout'), {
            'fields': ('template', 'col_lg', 'col_md', 'image', 'text_alignment', 'color', 'icon', 'card_type')
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'description', 'content', 'slug'),
        }),
    )
    ordering = ['order_index']
    prepopulated_fields = {"slug": ("title",)}
    extra = 0


class BookAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'get_product_image', 'get_product_category', 'template', 'created', 'modified', 'published', 'publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'book_product')
        }),
        (_('Layout'), {
            'fields': ('template', 'col_lg', 'col_md',)
        }),
        (_('Editing'), {
            'fields': ('title', 'short_title', 'description', 'lead', 'summary', 'slug', 'created', 'modified', 'publication_date'),
        }),
    )
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title']
    actions = [make_published, make_unpublished]
    save_as = True


class ChapterAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'order_index', 'chapter_book', 'created', 'modified',]
    fieldsets = (
        (_('Pubblication'), {
            'fields': ('chapter_book',)
        }),
        (_('Layout'), {
            'fields': ('image',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'description', 'slug', 'created', 'modified'),
        }),
    )
    readonly_fields = ['created', 'modified',]
    list_filter = ['chapter_book',]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order_index']
    search_fields = ['chapter_book__title']
    inlines = [SectionInline]


class SectionCategoryadmin(DiventiTranslationAdmin):
    list_display = ['title', 'default',]


admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(UniversalSection, UniversalSectionAdmin)
admin.site.register(Attachment, AttachmentAdmin)