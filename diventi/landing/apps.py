from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LandingConfig(AppConfig):
    name = 'diventi.landing'
    verbose_name = _('landing')
