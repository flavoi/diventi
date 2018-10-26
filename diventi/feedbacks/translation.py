from modeltranslation.translator import register, TranslationOptions

from .models import Survey, Question, Answer, SurveyCover, QuestionGroup, QuestionChoice


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


@register(SurveyCover)
class SurveyCoverTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(QuestionChoice)
class QuestionChoiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')