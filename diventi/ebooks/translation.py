from modeltranslation.translator import register, TranslationOptions

from .models import (
    Book, 
    Chapter, 
    Section, 
    UniversalSection, 
    Part, 
    ReplacementRule,
    SectionAspect,
    Secret,
)


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'paper_id', 'description', 'summary', 'slug')

@register(Part)
class PartTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'situation', 'slug')

@register(UniversalSection)
class UniversalSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)
    
@register(ReplacementRule)
class ReplacementRuleTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'initial_string', 'result_string')

@register(SectionAspect)
class SectionAspectTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Secret)
class SecretTranslationOptions(TranslationOptions):
    fields = ('title', 'description')