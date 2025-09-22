from modeltranslation.translator import register, TranslationOptions

from .models import IngestedDocument, GemmaIstruction, WelcomeMessage


@register(IngestedDocument)
class IngestedDocumentTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(GemmaIstruction)
class GemmaIstructionTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'slug', 'system_instruction', 'summary_istruction', 'character_sheet_istruction', 'welcome_message_istruction')


@register(WelcomeMessage)
class IngestedDocumentTranslationOptions(TranslationOptions):
    fields = ('bot_response',)