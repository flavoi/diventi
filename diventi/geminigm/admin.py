from django.contrib import admin
from .models import ChatMessage, IngestedDocument

admin.site.register(ChatMessage)
admin.site.register(IngestedDocument)