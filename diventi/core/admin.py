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

"""
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
"""