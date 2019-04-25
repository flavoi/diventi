from modeltranslation.translator import register, TranslationOptions

from .models import Section


@register(Section)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')