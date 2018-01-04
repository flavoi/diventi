from modeltranslation.translator import register, TranslationOptions

from .models import Presentation


@register(Presentation)
class PresentationTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'description')