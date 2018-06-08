from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin

admin.site.site_header = _("Diventi Control Panel")
admin.site.site_title = _("Diventi Control Panel")


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
