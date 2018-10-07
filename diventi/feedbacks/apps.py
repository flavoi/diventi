from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FeedbacksConfig(AppConfig):
    name = 'diventi.feedbacks'
    verbose_name = _('Feedbacks')
