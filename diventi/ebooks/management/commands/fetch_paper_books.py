from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from django.utils import translation

from diventi.ebooks.cron import fetch_paper_books

class Command(BaseCommand):
    help = _('Fetch the paper books from dropbox and export them in html format')

    def handle(self, *args, **options):
        fetch_paper_books()