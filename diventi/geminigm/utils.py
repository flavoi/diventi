# myapp/utils.py
from django.conf import settings
from .models import IngestedDocument, GemmaIstruction


def ingest_pdf_document(pdf_path: str, title: str, gemini_file_id=''):
    try:
        IngestedDocument.objects.create(title=title, file_path=pdf_path, gemini_file_id=gemini_file_id)
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


def user_has_access_to_ai(product, user):
    return product.user_has_already_bought(user) or product.user_has_authored(user) or (user.has_perm('accounts.can_playtest') and product.playtest_material)
