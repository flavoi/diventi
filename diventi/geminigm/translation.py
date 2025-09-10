from modeltranslation.translator import register, TranslationOptions

from .models import IngestedDocument, GemmaIstruction


@register(IngestedDocument)
class IngestedDocumentTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(GemmaIstruction)
class GemmaIstructionTranslationOptions(TranslationOptions):
    fields = ('title', 'system_instruction', 'summary_istruction', 'character_sheet_istruction', 'welcome_message_istruction')