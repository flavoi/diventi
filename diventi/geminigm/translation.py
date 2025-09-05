from modeltranslation.translator import register, TranslationOptions

from .models import IngestedDocument


@register(IngestedDocument)
class IngestedDocumentTranslationOptions(TranslationOptions):
    fields = ('title',)