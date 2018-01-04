from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

admin.site.site_header = "Diventi's Dashboard"
admin.site.site_title = "Diventi's Dashboard"


class DiventiTranslationAdmin(TranslationAdmin):

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }