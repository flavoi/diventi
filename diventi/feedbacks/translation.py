from modeltranslation.translator import register, TranslationOptions

from .models import (
    Survey, 
    Question, 
    Answer, 
    QuestionGroup, 
    QuestionChoice,
)


@register(Survey)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question', )


@register(QuestionGroup)
class QuestionGroupTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ('content', )


@register(QuestionChoice)
class QuestionChoiceTranslationOptions(TranslationOptions):
    fields = ('title', )