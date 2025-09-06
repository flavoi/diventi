from django.contrib import admin
from .models import ChatMessage, IngestedDocument

from diventi.core.admin import DiventiTranslationAdmin


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user_message', 'created_at', 'author']
    readonly_fields = ['created_at',]


class IngestedDocumentAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'ingested_at',]
    readonly_fields = ['ingested_at',]


admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(IngestedDocument, IngestedDocumentAdmin)


