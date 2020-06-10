from modeltranslation.translator import register, TranslationOptions

from .models import (
    Keyword,
    Tooltip,
)


@register(Keyword)
class KeywordTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Tooltip)
class TooltipTranslationOptions(TranslationOptions):
    fields = ('title',)