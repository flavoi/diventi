from modeltranslation.translator import register, TranslationOptions

from .models import CharacterSheet, Relationship


@register(CharacterSheet)
class CharacterSheetTranslationOptions(TranslationOptions):
    fields = ('name', 'origin', 'predisposition', 'slug')

@register(Relationship)
class RelationshipTranslationOptions(TranslationOptions):
    fields = ('title', 'description')