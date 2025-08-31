import os
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from django.conf import settings

from diventi.geminigm.models import IngestedDocument, ChatMessage


class Command(BaseCommand):
    help = _('Clean ingested entries and every chat messages')

    def handle(self, *args, **options):
        print(IngestedDocument.objects.all().delete())
        print(ChatMessage.objects.all().delete())
        print(shutil.rmtree(os.path.join(settings.PROJ_ROOT, 'chroma_db/')))