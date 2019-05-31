from modeltranslation.translator import register, TranslationOptions

from .models import Book, Chapter, Section, UniversalSection, SectionCategory


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)

@register(UniversalSection)
class UniversalSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)

@register(SectionCategory)
class SectionCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)
