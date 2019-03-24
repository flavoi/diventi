from modeltranslation.translator import register, TranslationOptions

from .models import Presentation, Feature


@register(Presentation)
class PresentationTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'description', 'projects_description', 'label', 'featured_label')


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)