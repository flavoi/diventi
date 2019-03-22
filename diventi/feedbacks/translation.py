from modeltranslation.translator import register, TranslationOptions

from .models import Survey, Question, Answer, QuestionGroup, QuestionChoice, Outcome


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


@register(Outcome)
class QuestionChoiceTranslationOptions(TranslationOptions):
    fields = ('title', 'upper_outcome', 'medium_outcome', 'lower_outcome')