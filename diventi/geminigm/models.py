from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f_("Player: {self.user_message}, GM: {self.bot_response}")

    class Meta:
        verbose_name = _('chat message')
        verbose_name_plural = _('chat messages')