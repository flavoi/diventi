from modeltranslation.translator import register, TranslationOptions

from diventi.core.admin import DiventiTranslationAdmin

from .models import Paper, Section, Watermark


@register(Paper)
class PaperTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Watermark)
class WatermarkTranslationOptions(TranslationOptions):
    fields = ('title',)
