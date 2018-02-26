from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import Product, Chapter, Characteristic, ImagePreview, ProductCategory, ChapterCategory

def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected products as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected products as hidden")


class ChapterInline(TranslationStackedInline):
    model = Chapter
    fields = ('title', 'description', 'image', 'category')
    extra = 0


class CharacteristicInline(TranslationStackedInline):
    model = Characteristic
    fields = ('title', 'description')
    extra = 0


class ImagePreviewInline(TranslationStackedInline):
    model = ImagePreview
    fields = ( 'label', 'image')
    extra = 0


class ImagePreviewAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag')


class ProductAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'featured', 'image_tag', 'published', 'publication_date']    
    inlines = [
        ChapterInline,
        CharacteristicInline,
        ImagePreviewInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['created', 'modified','publication_date']
    actions = [make_published, make_unpublished]


class CategoryAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'default')


admin.site.register(Product, ProductAdmin)
admin.site.register(ImagePreview, ImagePreviewAdmin)
admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(ChapterCategory, CategoryAdmin)
