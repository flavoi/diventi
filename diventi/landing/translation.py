from modeltranslation.translator import register, TranslationOptions

from .models import Presentation, Feature


@register(Presentation)
class PresentationTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'description',)


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)