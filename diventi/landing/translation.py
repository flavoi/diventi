from modeltranslation.translator import register, TranslationOptions

from .models import Presentation, Feature, About, AboutCover


@register(Presentation)
class PresentationTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'description',)


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(AboutCover)
class AboutCoverTranslationOptions(TranslationOptions):
    fields = ('label',)