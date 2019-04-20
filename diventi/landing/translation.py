from modeltranslation.translator import register, TranslationOptions

from .models import Feature, Section


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)