import os
import shutil
from google import genai

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from django.conf import settings

from diventi.geminigm.models import IngestedDocument, ChatMessage


class Command(BaseCommand):
    help = _('Ripulisce tutti i dati generati da IA in questa app')

    def handle(self, *args, **options):
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        for f in client.files.list():
            print(f"Elimino file {f.name}")
            client.files.delete(name=f.name)
        print(IngestedDocument.objects.all().delete())
        print(ChatMessage.objects.all().delete())
        print(shutil.rmtree(os.path.join(settings.PROJ_ROOT, 'chroma_db/')))
        