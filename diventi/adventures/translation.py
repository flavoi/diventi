from modeltranslation.translator import register, TranslationOptions

from .models import (
    Adventure,
    Situation,
    Match,
    Story,
)


@register(Adventure)
class AdventureTranslationOptions(TranslationOptions):
    fields = ('title',)