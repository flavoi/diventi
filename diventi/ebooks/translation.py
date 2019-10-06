from modeltranslation.translator import register, TranslationOptions

from .models import Book, Chapter, Section, UniversalSection, Attachment, Part


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'lead', 'summary', 'slug')

@register(Part)
class PartTranslationOptions(TranslationOptions):
    fields = ('title',)

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