from modeltranslation.translator import register, TranslationOptions

from diventi.core.admin import DiventiTranslationAdmin

from .models import Brew


@register(Brew)
class BrewTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')