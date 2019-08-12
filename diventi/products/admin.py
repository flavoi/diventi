from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import Product, Chapter, ImagePreview, ProductCategory, ChapterCategory
from .forms import ProductForm


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected products as published")

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected products as hidden")

def make_available(modeladmin, request, queryset):
    queryset.update(available=True)
make_available.short_description = _("Mark selected products as available")

def make_unavailable(modeladmin, request, queryset):
    queryset.update(available=False)
make_unavailable.short_description = _("Mark selected products as unavailable")


class ChapterInline(TranslationStackedInline):
    model = Chapter
    fields = ('title', 'description', 'category', 'icon')
    extra = 0


class ImagePreviewInline(TranslationStackedInline):
    model = ImagePreview
    fields = ( 'label', 'image')
    extra = 0


class ImagePreviewAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag')


class ProductAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'featured', 'published', 'available', 'publication_date', 'modified']    
    inlines = [
        ChapterInline,
        ImagePreviewInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['created', 'modified','publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'available', 'featured')
        }),
        (_('Editing'), {
            'fields': ('title', 'abstract', 'description', 'image', 'category', 'file', 'authors', 'buyers', 'courtesy_short_message', 'courtesy_message', 'slug'),
        }),
        (_('Related'), {
            'fields': ('related_products',),
        }),
    )
    actions = [make_published, make_unpublished, make_available, make_unavailable]
    raw_id_fields = ['buyers']
    form = ProductForm


class CategoryAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'default')


admin.site.register(Product, ProductAdmin)
admin.site.register(ImagePreview, ImagePreviewAdmin)
admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(ChapterCategory, CategoryAdmin)
