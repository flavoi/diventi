from modeltranslation.translator import register, TranslationOptions

from .models import Survey, Question, Answer


@register(Survey)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title', 'slug')


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question', )


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ('content', )

