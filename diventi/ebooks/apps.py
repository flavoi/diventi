from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EbooksConfig(AppConfig):
    name = 'diventi.ebooks'
    verbose_name = _('Ebooks')
