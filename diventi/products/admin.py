from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import Product, Chapter, ImagePreview, ProductCategory, ChapterCategory, Purchase, ProductDetail
from .forms import ProductForm


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected products as published")

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected products as hidden")


class ProductDetailInline(TranslationStackedInline):
    model = ProductDetail
    fields = ('title', 'description',)
    extra = 0


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


class PurchaseInline(admin.TabularInline):
    model = Purchase
    readonly_fields = ['created',]
    extra = 1


class ProductAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'published', 'price', 'category', 'publication_date', 'modified']    
    inlines = [
        ProductDetailInline,
        ChapterInline,
        ImagePreviewInline,
        PurchaseInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['created', 'modified','publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published',)
        }),
        (_('Pricing'), {
            'fields': ('price',)
        }),
        (_('Editing'), {
            'fields': ('title', 'abstract', 'description', 'image', 'category', 'file', 'authors', 'courtesy_short_message', 'courtesy_message', 'slug'),
        }),
        (_('Related'), {
            'fields': ('related_products',),
        }),
    )
    actions = [make_published, make_unpublished]
    form = ProductForm
    filter_horizontal = ['buyers']
    list_select_related = (
        'category',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)
        form.author_field = 'authors'
        return form


class ProductCategoryAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'meta_category')
    fields = ('title', 'meta_category')


class ChapterCategoryAdmin(DiventiTranslationAdmin):
    list_display = ('title',)
    fields = ('title',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ImagePreview, ImagePreviewAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ChapterCategory, ChapterCategoryAdmin)
