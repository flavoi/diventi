# myapp/utils.py
from django.conf import settings
from .models import IngestedDocument


# --- Funzioni di Ingestione ---

def ingest_pdf_document(pdf_path: str, title: str):
    try:
        IngestedDocument.objects.create(title=title, file_path=pdf_path)
        return True, f"PDF '{title}' ingestito con successo (incluse tabelle e elementi di liste)."
    except Exception as e:
        return False, f"Errore durante l'ingestione del PDF: {e}"


def ingest_website_document(url: str, title: str):
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        IngestedDocument.objects.create(title=title, source_url=url)
        return True, f"Sito web '{title}' da {url} ingestito con successo."

    except Exception as e:
        return False, f"Errore durante l'ingestione del sito web: {e}"