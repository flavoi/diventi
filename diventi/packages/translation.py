from modeltranslation.translator import register, TranslationOptions

from .models import (
    Package,
)


@register(Package)
class PackageCoverTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'courtesy_short_message', 'courtesy_message', 'slug')