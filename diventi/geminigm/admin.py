from django.contrib import admin
from .models import (
    ChatMessage, 
    IngestedDocument,
    GemmaIstruction,
    WelcomeMessage,
)

from diventi.core.admin import DiventiTranslationAdmin


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user_message', 'created_at', 'author']
    readonly_fields = ['created_at',]
    search_fields = ('author__first_name','author__email','author__nametag')
    ordering = ('-created_at',)


class IngestedDocumentAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'ingested_at',]
    readonly_fields = ['ingested_at',]


class GemmaIstructionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'active', 'created_at',]
    readonly_fields = ['created_at',]
    prepopulated_fields = {"slug": ("title",)}
    

class WelcomeMessageAdmin(DiventiTranslationAdmin):
    list_display = ['bot_response', 'created_at',]
    readonly_fields = ['created_at',]


admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(IngestedDocument, IngestedDocumentAdmin)
admin.site.register(GemmaIstruction, GemmaIstructionAdmin)
admin.site.register(WelcomeMessage, WelcomeMessageAdmin)


