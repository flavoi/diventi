from modeltranslation.translator import register, TranslationOptions

from .models import Book, Chapter, Section, UniversalSection, Attachment


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'lead', 'summary', 'slug')

@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')

@register(UniversalSection)
class UniversalSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)

@register(Attachment)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)