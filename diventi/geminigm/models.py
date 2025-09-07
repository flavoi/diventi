from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class ChatMessage(models.Model):
    user_message = models.TextField(
        verbose_name=_('user message'),
    )
    bot_response = models.TextField(
        verbose_name=_('bot response'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        verbose_name=_('author'),
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation date'),
    )

    def __str__(self):
        return self.user_message

    class Meta:
        verbose_name = _('chat message')
        verbose_name_plural = _('chat messages')


class IngestedDocument(models.Model):
    title = models.CharField(
        max_length=255, 
        verbose_name=_('title')
    )
    source_url = models.URLField(
        max_length=2000, 
        null=True, 
        blank=True,
        verbose_name=_('source url')
    )
    file_path = models.CharField(
        max_length=1000, 
        null=True, 
        blank=True,
        verbose_name=_('file path'),
    )
    gemini_file_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        verbose_name=_('ID file Gemini'),
    )
    ingested_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('ingestion date'),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('ingested document')
        verbose_name_plural = _('ingested documents')


class GemmaIstructionQuerySet(models.QuerySet):

    # Returns the latest gemma that has active status
    def active(self):
        gemma = self.order_by('created_at')
        gemma = gemma.filter(active=True)
        gemma = gemma.first()
        return gemma


class GemmaIstruction(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name=_('title'),
    )
    description = models.TextField(
        verbose_name=_('description'),
    )
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('ingestion date'),
    )

    objects = GemmaIstructionQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Gemma istruction')
        verbose_name_plural = _('Gemma istructions')


class WelcomeMessage(models.Model):
    bot_response = models.TextField(
        verbose_name=_('bot response'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation date'),
    )

    def __str__(self):
        return self.bot_response

    class Meta:
        verbose_name = _('Welcome message')
        verbose_name_plural = _('Welcome messages')
