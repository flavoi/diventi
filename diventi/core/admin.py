from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin


admin.site.site_header = _("Diventi Control Panel")
admin.site.site_title = _("Diventi Control Panel")


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected items as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected items as hidden")


def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)
deactivate.short_description = _("Mark selected items for deactivation")


def duplicate(modeladmin, request, queryset):
    for model in queryset:
        model.duplicate()
duplicate.short_description = _("Duplicate selected items")


class DiventiTranslationAdmin(TabbedTranslationAdmin):
    pass


class DiventiIconAdmin(admin.ModelAdmin):
    
    class Media:
        css = {
            'all': ('diventi/css/diventi-admin-colors.css',)
        }
        js = ('quick-v110/libs/feather-icons/dist/feather.min.js', 'diventi/js/diventi-admin.js')

        