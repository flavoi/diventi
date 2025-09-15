from google import genai
from google.genai import types

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils import translation

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
                print(f"Documento locale {d.gemini_file_id} presente anche in gemini, nessuna azione necessaria")
            except Exception as e:
                print(f"File {d.gemini_file_id} non trovato, lo ricarico in Gemini e mi annoto nuovo ID")
                gemini_file = client.files.upload(file=d.file_path)
                d.gemini_file_id = gemini_file.name
                d.save()
                print(f"Caricato nuovo file {d.gemini_file_id} da {d.file_path}")

        wm = WelcomeMessage.objects.create()

        # Genera un nuovo messaggio di benvenuto in lingua IT
        translation.activate('it')
        contents_for_gemini = []
        gemma = GemmaIstruction.objects.active()
        contents_for_gemini.append(gemma.system_instruction)
        contents_for_gemini.append(gemma.welcome_message_istruction)
        for f_gemini in client.files.list():
            contents_for_gemini.append(f_gemini)

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=contents_for_gemini,
            )
            response_text_it = response.text
            wm.bot_response = response_text_it
            wm.save()
            print(f"Nuovo messaggio di benvenuto IT generato con successo")
            translation.activate('en')
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=f'traduci in inglese "{response_text_it}". Non tradurre Primo Contatto e non riportare frasi come "ecco la traduzione", riporta direttamente il risultato',
            )
            wm.bot_response=response.text
            wm.save()
            print(f"Nuovo messaggio di benvenuto EN generato con successo")
        except Exception as e:
            print(f"Errore durante la generazione della risposta da Gemini: {e}")
        
        