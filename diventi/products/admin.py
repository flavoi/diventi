from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import (
    DiventiIconAdmin,
    DiventiTranslationAdmin,
)

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import (
    Product, 
    Chapter, 
    ImagePreview, 
    ProductCategory, 
    ChapterCategory, 
    Purchase, 
    ProductDetail, 
    ProductFormat,
)
from .forms import ProductForm


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected products as published")

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected products as hidden")


class ProductDetailInline(TranslationStackedInline):
    model = ProductDetail
    fields = ('title', 'description', 'highlighted')
    extra = 0


class ProductFormatAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    model = ProductFormat
    list_display = ['title', 'icon_tag', 'color_tag']
    fields = ('title', 'description', 'icon', 'icon_style', 'color')    
    extra = 0


class ChapterInline(TranslationStackedInline):
    model = Chapter
    fields = ('title', 'description', 'icon', 'icon_style', 'color')
    extra = 0


class ImagePreviewInline(TranslationStackedInline):
    model = ImagePreview
    fields = ('title', 'description', 'image')
    extra = 0


class ImagePreviewAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'image_tag', 'product')
    fields = ('title', 'description', 'image', 'product')


class ProductAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'published', 'unfolded', 'pinned', 'hot', '_at_a_premium', 'public', 'product_survey', 'category', 'publication_date', 'modified']    
    inlines = [
        ChapterInline,
        ImagePreviewInline,
        ProductDetailInline,        
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['created', 'modified','publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'unfolded', 'product_survey', 'hot', 'pinned', 'public')
        }),
        (_('Layout'), {
            'fields': ('col_lg', 'order_lg', 'col_md', 'order_md', 'col_sm', 'order_sm',)
        }),
        (_('Pricing'), {
            'fields': ('stripe_product', 'stripe_price',)
        }),
        (_('Editing'), {
            'fields': ('title', 'short_description', 'abstract', 'description', 'image', 'category', 'file', 'authors', 'formats', 'courtesy_short_message', 'courtesy_message', 'slug'),
        }),
        (_('Related'), {
            'fields': ('related_products',),
        }),
    )
    actions = [make_published, make_unpublished]
    form = ProductForm
    list_select_related = (
        'category',
    )
    ordering = ('-published', '-unfolded',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)
        form.author_field = 'authors'
        return form


class ProductCategoryAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    list_display = ('title', 'icon_tag', 'color_tag', 'meta_category')
    fieldsets = (
        (_('Management'), {
            'fields': ('meta_category',)
        }),
        (_('Multimedia'), {
            'fields': ('icon', 'color'),
        }),
        (_('Editing'), {
            'fields': ('title', 'description', 'slug'),
        }),
    )
    prepopulated_fields = {"slug": ("title",)}


class ChapterCategoryAdmin(DiventiTranslationAdmin):
    list_display = ('title',)
    fields = ('title',)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'product', 'created')
    readonly_fields = ['created',]
    search_fields = ['customer__first_name']
    list_filter = ['product',]


admin.site.register(Product, ProductAdmin)
admin.site.register(ImagePreview, ImagePreviewAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ProductFormat, ProductFormatAdmin)
