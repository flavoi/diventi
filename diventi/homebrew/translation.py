from modeltranslation.translator import register, TranslationOptions

from diventi.core.admin import DiventiTranslationAdmin

from .models import Paper, Section


@register(Paper)
class PaperTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')