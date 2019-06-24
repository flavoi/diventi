from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SheetsConfig(AppConfig):
    name = 'diventi.sheets'
    verbose_name = _('Sheets')
