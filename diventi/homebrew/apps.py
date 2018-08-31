from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HomebrewConfig(AppConfig):
    name = 'diventi.homebrew'
    verbose_name = _('Homebrew')
