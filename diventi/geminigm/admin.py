from django.contrib import admin
from .models import (
    ChatMessage, 
    IngestedDocument,
    GemmaIstruction,
    WelcomeMessage,
    SectionAddon,
)

from diventi.core.admin import DiventiTranslationAdmin


class SectionAddonAdmin(admin.ModelAdmin):
    list_display = ('title', 'addon_template', 'enable_ai')
    list_filter = ('addon_template', 'enable_ai')
    search_fields = ('title', 'addon_template')
    prepopulated_fields = {"slug": ("title",)}


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user_message', 'created_at', 'author', 'gemma']
    readonly_fields = ['created_at',]
    search_fields = ('author__first_name','author__email','author__nametag', 'gemma__title')
    ordering = ('-created_at',)


class IngestedDocumentAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'ingested_at',]
    readonly_fields = ['ingested_at',]


class GemmaIstructionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'active', 'created_at',]
    readonly_fields = ['created_at',]
    prepopulated_fields = {"slug": ("title",)}
    

class WelcomeMessageAdmin(DiventiTranslationAdmin):
    list_display = ['bot_response', 'created_at', 'gemma']
    readonly_fields = ['created_at',]


admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(IngestedDocument, IngestedDocumentAdmin)
admin.site.register(GemmaIstruction, GemmaIstructionAdmin)
admin.site.register(WelcomeMessage, WelcomeMessageAdmin)
admin.site.register(SectionAddon, SectionAddonAdmin)


