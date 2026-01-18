from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import (
    DiventiIconAdmin,
    DiventiTranslationAdmin,
    deactivate,
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
    ProductCover,
    ProductImage,
    ProductDownloadSession,
)
from .forms import ProductForm


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected products as published")

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected products as hidden")


class ChapterDetailInline(TranslationStackedInline):
    model = Chapter
    fields = ('title', 'description', 'icon', 'color')
    extra = 0


class ProductDetailInline(TranslationStackedInline):
    model = ProductDetail
    fields = ('title', 'description', 'icon', 'highlighted')
    extra = 0


class ProductFormatAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    model = ProductFormat
    list_display = ['title', 'icon_tag', 'color_tag']
    fields = ('title', 'description', 'icon', 'color')
    extra = 0


class ProductAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'cover_primary_tag', 'cover_secondary_tag', 'published', 'unfolded', 'pinned', 'featured', 'public', 'playtest_material', 'category', 'publication_date', 'modified']    
    inlines = [
        ProductDetailInline, 
        ChapterDetailInline,       
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['created', 'modified','publication_date']
    fieldsets = (
        (_('Content'), {
            'fields': ('file',)
        }),
        (_('Management'), {
            'fields': ('published', 'unfolded', 'pinned', 'featured', 'public', 'playtest_material')
        }),
        (_('Pricing'), {
            'fields': ('stripe_product', 'stripe_price',)
        }),
        (_('Multimedia'), {
            'fields': ('cover_primary', 'cover_secondary'),
        }),
        (_('Editing'), {
            'fields': ('title', 'short_description', 'abstract', 'description', 'category', 'authors', 'formats', 'courtesy_short_message', 'courtesy_message', 'slug'),
        }),
        (_('Related'), {
            'fields': ('related_products', 'related_articles', 'related_forum_topic'),
        }),
    )
    actions = [make_published, make_unpublished]
    list_filter = ['category',]
    form = ProductForm
    list_select_related = (
        'category',
    )
    ordering = ('-published', '-unfolded',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)
        form.author_field = 'authors'
        return form

    def cover_primary_tag(self, obj):
        if obj.cover_primary:
            return obj.cover_primary.image_tag()
        else:
            return '-'
    cover_primary_tag.short_description = _('primary cover')

    def cover_secondary_tag(self, obj):
        if obj.cover_secondary:
            return obj.cover_secondary.image_tag()
        else:
            return '-'
    cover_secondary_tag.short_description = _('secondary cover')


class ProductCategoryAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    list_display = ('title', 'color_tag', 'meta_category')
    fieldsets = (
        (_('Management'), {
            'fields': ('meta_category',)
        }),
        (_('Multimedia'), {
            'fields': ('color',),
        }),
        (_('Editing'), {
            'fields': ('title', 'title_plural', 'slug'),
        }),
    )
    prepopulated_fields = {"slug": ("title",)}


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'product', 'created')
    readonly_fields = ['created',]
    search_fields = ['customer__first_name']
    list_filter = ['product',]
    raw_id_fields = ('customer', )


class ProductCoverAdmin(DiventiTranslationAdmin):
    list_display= ('title', 'description', 'image_tag', 'active')
    fieldsets = (
        (_('Management'), {
            'fields': ('active',)
        }),
        (_('Editing'), {
            'fields': ('title', 'image', 'description',),
        }),
    )
    actions = [deactivate]


class ProductDownloadSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'product', 'created', 'user', 'stripe_email', 'is_valid')
    search_fields = ['user__first_name', 'user__nametag', 'product__title', 'product__slug', 'stripe_email']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ProductFormat, ProductFormatAdmin)
admin.site.register(ProductCover, ProductCoverAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductDownloadSession, ProductDownloadSessionAdmin)