from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TooltipsConfig(AppConfig):
    name = 'diventi.tooltips'
    verbose_name = _('Tooltips')