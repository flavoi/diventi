import os, markdown
from google import genai
from google.genai import types

from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages

from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required

from .models import ChatMessage, IngestedDocument, WelcomeMessage
from .forms import PDFUploadForm, WebIngestionForm
from .utils import ingest_pdf_document, ingest_website_document


GEMMA = _("Sei un game master (GM) che deve gestire un gioco di ruolo da tavolo con ambientazione e meccaniche personalizzate denominato Primo Contatto (che trovi in allegato).  Tratta la conversazione come una sessione di gioco continua, ricordandoti tutti i dettagli che andranno via via emergendo. Tu genererai e descriverai (in maniera concisa ma evocativa) il mondo, gli eventi e gli esiti delle azioni di Personaggi Giocanti (PG) e Personaggi Non Giocanti (PNG). Deciderai anche come i PNG agiranno. Questa chat dovrà essere inclusa nel tuo contesto per generare le risposte, per cui dovrai ricordarti esattamente gli eventi che andranno verificandosi e i nomi/descrizioni dei luoghi e dei personaggi. \
Alcune note per il GM: rimani sempre in gioco come GM del gioco di ruolo, tu sei in controllo e sei responsabile di come il gioco evolverà. Cerca di mantenere le risposte concise e chiare. Evidenzia nomi, luoghi, oggetti. Le decisioni prese dovrebbero avere conseguenze e peso. Fornisci frequenti spunti narrativi per i giocatori e suggerisci possibili azioni che i personaggi potrebbero intraprendere. Usa creatività e varietà quando generi dei nomi di cose o persone. Non generarne di troppo simili. \
Il tema: la campagna è ambientata nel mondo di Primo Contatto, un pianeta Terra alternativo in cui nell'anno 2020 è caduto un oggetto celeste in Sud America, disattivando in tutte le Americhe la tecnologia come la conosciamo oggi. In quel giorno fatidico alcune persone hanno visto nascere dei poteri magici dentro di loro, chiamati doti.\
Rispetto delle regole: Segui scrupolosamente le regole del manuale che ti è stato fornito, con le seguenti eccezioni e adattamenti specifici che abbiamo stabilito durante la sessione:\
Improvvisazione: In caso di domande o azioni non previste dal manuale, improvvisa risposte che si allineino al tono e al tema del gioco.\
Evitare il metagioco: Non rivelare statistiche esatte di nemici o esiti di prove. Descrivi gli eventi in modo narrativo, lasciando che i giocatori scoprano i dettagli.\
Azione Combinata: Per un'azione combinata, ogni giocatore deve superare la propria prova. Se un giocatore ha un successo eccezionale, può compensare un risultato inferiore di un altro, a discrezione del GM.")


@staff_member_required
def ingest_document_view(request):
    pdf_form = PDFUploadForm()
    web_form = WebIngestionForm()
    ingested_docs = IngestedDocument.objects.all().order_by('-ingested_at')

    if request.method == 'POST':
        if 'upload_pdf' in request.POST:
            pdf_form = PDFUploadForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                pdf_file = request.FILES['pdf_file']
                title = pdf_form.cleaned_data['title']

                # Salva temporaneamente il PDF in MEDIA_ROOT
                upload_dir = os.path.join(settings.GEMINI_INJESTION_MEDIA, 'temp_pdfs')
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, pdf_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in pdf_file.chunks():
                        destination.write(chunk)

                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                gemini_file_id = client.files.upload(file=file_path)
                success, msg = ingest_pdf_document(file_path, title, gemini_file_id.name)
                if success:
                    messages.success(request, msg)
                else:
                    messages.error(request, msg)
                return redirect('geminigm:ingest_document') # Ricarica la pagina per mostrare i messaggi

        elif 'ingest_web' in request.POST:
            web_form = WebIngestionForm(request.POST)
            if web_form.is_valid():
                url = web_form.cleaned_data['url']
                title = web_form.cleaned_data['title']
                success, msg = ingest_website_document(url, title)
                if success:
                    messages.success(request, msg)
                else:
                    messages.error(request, msg)
                return redirect('geminigm:ingest_document') # Ricarica la pagina per mostrare i messaggi

    context = {
        'pdf_form': pdf_form,
        'web_form': web_form,
        'ingested_docs': ingested_docs,
    }
    return render(request, 'geminigm/ingest_document.html', context)


@staff_member_required
def chatbot_view(request):
    response_text = ""
    query = ""
    contents_for_gemini = []

    if request.method == 'POST':
        query = request.POST.get('query', '')
        
        if query:

            try:
                client = genai.Client(api_key=settings.GEMINI_API_KEY)

                chat_messages = ChatMessage.objects.filter(author=request.user).order_by('created_at')
                for m in chat_messages:
                    contents_for_gemini.append(
                        f'Messaggio utente: {m.user_message} del {m.created_at}',
                    )
                    contents_for_gemini.append(
                        f'Risposta del sistema: {m.bot_response} del {m.created_at}',
                    )
                
                for f_gemini in client.files.list():
                    contents_for_gemini.append(f_gemini)

                contents_for_gemini.append(
                    f"Dati i file allegati, le istruzioni di sistema e la cronologia dei messaggi, rispondi alla domanda dell'utente: {query}.",
                )
                contents_for_gemini.append(
                    f"Se non riesci a recuperare le informazioni necessarie dichiaralo e improvvisa contenuti usando ciò che hai.",
                )
                            
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    #model='gemini-2.5-flash',
                    #model ='gemini-1.5-flash',
                    contents=contents_for_gemini,
                    config=types.GenerateContentConfig(
                        system_instruction=GEMMA),
                )
                response_text = response.text
                ChatMessage.objects.create(user_message=query, bot_response=response_text, author=request.user)
            except Exception as e:
                response_text = f"Errore durante la generazione della risposta da Gemini: {e}"
    else:
        try:
            response_text = WelcomeMessage.objects.latest('created_at').bot_response
                      
        except Exception as e:
            response_text = f"Errore durante la generazione della risposta da Gemini: {e}"
    
    context = {
        'response_text': markdown.markdown(response_text),
        'query': query,
    }
    return render(request, 'geminigm/chatbot.html', context)

