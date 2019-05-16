from modeltranslation.translator import register, TranslationOptions

from .models import Book, Chapter, Section, UniversalSection


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')

@register(UniversalSection)
class UniversalSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)