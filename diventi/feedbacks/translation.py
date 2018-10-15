from modeltranslation.translator import register, TranslationOptions

from .models import Survey, Question, Answer, SurveyCover


@register(Survey)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'label', 'slug')


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question', )


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ('content', )


@register(SurveyCover)
class SurveyCoverTranslationOptions(TranslationOptions):
    fields = ('label',)