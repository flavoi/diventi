from modeltranslation.translator import register, TranslationOptions

from .models import Chapter, Section


@register(Chapter)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


@register(Section)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')