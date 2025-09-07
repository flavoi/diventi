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
            if client.files.get(name=d.gemini_file_id):
                print(f"Documento locale {d.gemini_file_id} presente anche in gemini")
            else:
                gemini_file = client.files.upload(d.file_path)
                d.gemini_file_id = gemini_file.name

        # Rigenera un nuovo messaggio di benvenuto
        contents_for_gemini = []
        for f_gemini in client.files.list():
            contents_for_gemini.append(f_gemini)
        contents_for_gemini.append('Mostra un breve messaggio di benvenuto con un riepilogo del gioco. Massimo due paragrafi.')
        gemma = GemmaIstruction.objects.active()
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            #model='gemini-2.5-flash',
            #model ='gemini-1.5-flash',
            contents=contents_for_gemini,
            config=types.GenerateContentConfig(
                system_instruction=gemma),
        )
        print(WelcomeMessage.objects.create(bot_response=response.text))
        
        