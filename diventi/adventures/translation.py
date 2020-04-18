from modeltranslation.translator import register, TranslationOptions

from .models import (
    Adventure,
    Resolution,
)


@register(Adventure)
class AdventureTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Resolution)
class ResolutionTranslationOptions(TranslationOptions):
    fields = ('title',)