from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import (
    DiventiTranslationAdmin,
    deactivate,
)

from .models import (
    Package,
)


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected products as published")

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected products as hidden")


class PackageAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'published', 'pinned', 'publication_date', 'modified']    
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['created', 'modified','publication_date']
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'pinned',)
        }),
        (_('Pricing'), {
            'fields': ('stripe_product', 'stripe_price',)
        }),
        (_('Editing'), {
            'fields': ('title', 'description', 'courtesy_short_message', 'courtesy_message', 'slug'),
        }),
        (_('Related'), {
            'fields': ('related_products',),
        }),
    )
    actions = [make_published, make_unpublished]
    ordering = ('-published',)


admin.site.register(Package, PackageAdmin)