from modeltranslation.translator import register, TranslationOptions

from .models import (
    Adventure,
    Resolution,
    Antagonist,
    AntagonistGoal,
)


@register(Adventure)
class AdventureTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Resolution)
class ResolutionTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(AntagonistGoal)
class AntagonistGoalTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Antagonist)
class AntagonistTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)