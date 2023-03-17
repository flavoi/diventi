from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from diventi.core.admin import (
    DiventiTranslationAdmin,
    DiventiIconAdmin,
    deactivate,
)

from .models import (
    Package,
    FAQ,
)


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected products as published")

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected products as hidden")


class FAQAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'icon', 'package', 'modified']
    readonly_fields = ['created', 'modified',]
    list_filter = ['package',]
    fieldsets = (
        (_('Editing'), {
        'fields': ('title', 'answer',),
        }),
        (_('Multimedia'), {
            'fields': ('icon', 'color'),
        }),
        (_('Related'), {
            'fields': ('package',),
        }),
    )


class FAQInline(TranslationStackedInline):
    model = FAQ
    fields = ('title', 'answer', 'icon', 'color')
    extra = 0


class PackageAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'published', 'pinned', 'featured', 'get_hitcounts', 'publication_date', 'modified']    
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['created', 'modified','publication_date']
    inlines = [
        FAQInline,
    ]
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'pinned', 'featured',)
        }),
        (_('Pricing'), {
            'fields': ('stripe_product', 'stripe_price',)
        }),
        (_('Editing'), {
        'fields': ('title', 'short_description', 'abstract', 'description', 'courtesy_short_message', 'courtesy_message', 'slug'),
        }),
        (_('Related'), {
            'fields': ('related_products',),
        }),
    )
    actions = [make_published, make_unpublished]
    ordering = ('-published',)


admin.site.register(Package, PackageAdmin)
admin.site.register(FAQ, FAQAdmin)