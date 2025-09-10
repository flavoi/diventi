from google import genai
from google.genai import types

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from django.conf import settings

from diventi.geminigm.models import (
    IngestedDocument,
    GemmaIstruction,
    WelcomeMessage,
)


class Command(BaseCommand):
    help = _('Verifica i file caricati in gemini e crea un nuovo messaggio di benvenuto')

    def handle(self, *args, **options):
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # Verifica che i documenti ingestiti siano presenti in Gemini e se non lo sono li ricarica
        for d in IngestedDocument.objects.all():
            try:
                client.files.get(name=d.gemini_file_id)
                print(f"Documento locale {d.gemini_file_id} presente anche in gemini")
            except Exception as e:
                print(e)
                gemini_file = client.files.upload(file=d.file_path)
                d.gemini_file_id = gemini_file.name
                print(f"Caricato nuovo file {d.gemini_file_id} da {d.file_path}")

        # Rigenera un nuovo messaggio di benvenuto
        contents_for_gemini = []
        gemma = GemmaIstruction.objects.active()

        # Passa le istruzioni di sistema
        contents_for_gemini.append(gemma.system_instruction)

        # Aggiungi i file ingestiti come contesto
        for f_gemini in client.files.list():
            contents_for_gemini.append(f_gemini)

        contents_for_gemini.append(gemma.welcome_message_istruction)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=contents_for_gemini,
        )
        
        