from modeltranslation.translator import translator, register, TranslationOptions

from .models import Book, Chapter, Section, UniversalSection


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')

@register(UniversalSection)
class UniversalSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)


translator.register(Section, SectionTranslationOptions)