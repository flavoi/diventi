from modeltranslation.translator import register, TranslationOptions

from .models import (
    Package,
    FAQ,
)


@register(Package)
class PackageCoverTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'abstract', 'description', 'courtesy_short_message', 'courtesy_message', 'slug')


@register(FAQ)
class FAQCoverTranslationOptions(TranslationOptions):
    fields = ('title', 'answer',)