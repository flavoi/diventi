from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdventuresConfig(AppConfig):
    name = 'diventi.adventures'
    verbose_name = _('Adventures')
