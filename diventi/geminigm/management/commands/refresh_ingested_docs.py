import os
import shutil
from google import genai

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from django.conf import settings

from diventi.geminigm.models import IngestedDocument


class Command(BaseCommand):
    help = _('Verifica che i documenti ingestiti siano presenti in Gemini e se non lo sono li ricaricas.')

    def handle(self, *args, **options):
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        for d in IngestedDocument.objects.all():
            if client.files.get(name=d.gemini_file_id):
                print(f"Documento locale {d.gemini_file_id} presente anche in gemini")
            else:
                gemini_file = client.files.upload(d.file_path)
                d.gemini_file_id = gemini_file.name

        
        