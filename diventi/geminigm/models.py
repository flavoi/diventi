from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

from cuser.middleware import CuserMiddleware

from diventi.products.models import Product


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
        return gemma

    # Fetch the product related to the gemma
    def product(self):
        gemma = self.select_related('gemma_product')
        return gemma

    def playable(self, user):
        gemma = self.active().product()
        gemma_public = gemma.filter(gemma_product__public=True)
        gemma_playtest = gemma.none()
        if user.has_perm('accounts.can_playtest'):
            gemma_playtest = gemma.filter(gemma_product__playtest_material=True)
        gemma = gemma_public | gemma_playtest
        return gemma


class GemmaIstruction(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name=_('title'),
    )
    short_description = models.TextField(
        blank=True, 
        max_length=50, 
        verbose_name=_('short description')
    )
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('slug'),
    )
    system_instruction = models.TextField(
        verbose_name=_('system istruction'),
    )
    summary_istruction = models.TextField(
        verbose_name=_('summary istruction'),
    )
    character_sheet_istruction = models.TextField(
        verbose_name=_('character sheet istruction'),
    )
    welcome_message_istruction = models.TextField(
        verbose_name=_('welcome message istruction')
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_('active'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation date'),
    )
    gemma_product = models.OneToOneField(
        Product, 
        null = True, 
        blank = True, 
        related_name = 'gemma', 
        on_delete = models.SET_NULL, 
        verbose_name = _('product'),
    )

    objects = GemmaIstructionQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('geminigm:gemma_private', args=[self.slug,])

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
    gemma = models.ForeignKey(
        GemmaIstruction, 
        null = True, 
        related_name = 'welcome_messages', 
        verbose_name = _('gemma'), 
        on_delete = models.SET_NULL,
    )

    def __str__(self):
        return self.bot_response

    class Meta:
        verbose_name = _('Welcome message')
        verbose_name_plural = _('Welcome messages')


class ChatMessageQuerySet(models.QuerySet):

    # Fetch the last HISTORY_DEPTH messages relevant for the selected AI agent (gemma)
    def history(self, gemma):
        HISTORY_DEPTH = 85
        current_user = CuserMiddleware.get_user() # The user that is operating in the session
        messages = self.filter(gemma=gemma)
        messages = messages.filter(author=current_user)
        messages = messages.order_by('-created_at')[:HISTORY_DEPTH]
        return messages


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
    gemma = models.ForeignKey(
        GemmaIstruction, 
        null = True, 
        related_name = 'chat_messages', 
        verbose_name = _('gemma'), 
        on_delete = models.SET_NULL,
    )

    objects = ChatMessageQuerySet.as_manager()

    def __str__(self):
        return self.user_message

    class Meta:
        verbose_name = _('chat message')
        verbose_name_plural = _('chat messages')
