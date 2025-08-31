# myapp/utils.py
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

from django.conf import settings
from .models import IngestedDocument


# Inizializza il modello di embedding
# 'models/embedding-001' è il modello di embedding predefinito di LangChain per Gemini
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",  google_api_key=settings.GEMINI_API_KEY,)

# --- Configurazione del Database Vettoriale (Esempio con ChromaDB locale) ---
# Per un ambiente di produzione, useresti un servizio cloud come Pinecone, Weaviate, o un'istanza di ChromaDB.
# Installare: pip install chromadb langchain-chroma
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

# Funzione per ottenere o creare la collezione ChromaDB
def get_vector_store():
    # Persistent client per salvare su disco
    return Chroma(
        collection_name="my_chatbot_knowledge_base",
        embedding_function=embeddings_model,
        persist_directory=os.path.join(settings.PROJ_ROOT, 'chroma_db') # Salva in una cartella locale
    )

# --- Funzioni di Ingestione ---

def ingest_pdf_document(pdf_path: str, title: str):
    """
    Ingesta un documento PDF: estrae testo, lo chunkerizza, genera embedding e li salva nel DB vettoriale.
    """
    try:
        # Carica il PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Splitta il testo in chunk
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # Salva gli embedding nel database vettoriale
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        # vector_store.persist() # Salva le modifiche (se usi un client persistente)

        # Registra il documento nel tuo modello Django
        IngestedDocument.objects.create(title=title, file_path=pdf_path)
        return True, f"PDF '{title}' ingestito con successo."

    except Exception as e:
        return False, f"Errore durante l'ingestione del PDF: {e}"


def ingest_website_document(url: str, title: str):
    """
    Ingesta una pagina web: estrae testo, lo chunkerizza, genera embedding e li salva nel DB vettoriale.
    """
    try:
        # Carica la pagina web
        loader = WebBaseLoader(url)
        documents = loader.load()

        # Splitta il testo in chunk
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # Salva gli embedding nel database vettoriale
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        vector_store.persist() # Salva le modifiche (se usi un client persistente)

        # Registra il documento nel tuo modello Django
        IngestedDocument.objects.create(title=title, source_url=url)
        return True, f"Sito web '{title}' da {url} ingestito con successo."

    except Exception as e:
        return False, f"Errore durante l'ingestione del sito web: {e}"


# Funzione di esempio per interrogare il DB vettoriale
def query_knowledge_base(query_text: str):
    """
    Interroga la base di conoscenza vettoriale con una query testuale.
    Restituisce i chunk più rilevanti.
    """
    vector_store = get_vector_store()
    # Esegue una ricerca di similarità
    relevant_chunks = vector_store.similarity_search(query_text, k=3) # Restituisce i 3 chunk più rilevanti
    return relevant_chunks