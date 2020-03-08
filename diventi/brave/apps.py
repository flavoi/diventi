from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BraveConfig(AppConfig):
    name = 'diventi.brave'
    verbose_name = _('Brave')
