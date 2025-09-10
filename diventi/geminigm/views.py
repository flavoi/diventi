import os, markdown
import json # Importa il modulo json
from google import genai
from google.genai import types

from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse # Importa JsonResponse
from django.views.decorators.csrf import csrf_exempt # Potrebbe servire per i test, ma è meglio gestirlo con i token CSRF di Django

from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required

from .models import (
    ChatMessage,
    IngestedDocument,
    WelcomeMessage,
    GemmaIstruction,
)
from .forms import PDFUploadForm, WebIngestionForm
from .utils import ingest_pdf_document, ingest_website_document



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
    # Questa view ora serve solo per caricare la pagina iniziale della chat
    welcome_message = ""
    try:
        welcome_message = WelcomeMessage.objects.latest('created_at').bot_response
    except WelcomeMessage.DoesNotExist:
        welcome_message = "Benvenuto nella tua avventura di Primo Contatto!"

    context = {
        'welcome_message': markdown.markdown(welcome_message),
    }
    return render(request, 'geminigm/chatbot.html', context)


@staff_member_required
#@csrf_exempt # Rimuovi questa riga in produzione e usa i token CSRF
def send_message_ajax(request):
    if request.method == 'POST':
        query = request.POST.get('query', '') # Prendi la query dal corpo della richiesta POST

        if query:
            try:
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                gemma = GemmaIstruction.objects.active()

                contents_for_gemini = []

                # Passa le istruzioni di sistema
                contents_for_gemini.append(gemma.system_instruction)

                # Ottieni solo gli ultimi N messaggi per limitare la cronologia e non saturare il contesto
                chat_messages = ChatMessage.objects.filter(author=request.user).order_by('-created_at')[:100]
                # Inverti l'ordine per avere i messaggi più vecchi prima
                for m in reversed(chat_messages):
                    contents_for_gemini.append(f'Messaggio utente: {m.user_message}')
                    contents_for_gemini.append(f'Risposta del sistema: {m.bot_response}')

                # Aggiungi i file ingestiti come contesto
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
                    contents=contents_for_gemini,
                )
                response_text = response.text
                ChatMessage.objects.create(user_message=query, bot_response=response_text, author=request.user)

                return JsonResponse({
                    'success': True, 
                    'bot_response': markdown.markdown(response_text),
                })

            except Exception as e:
                error_message = f"Errore durante la generazione della risposta da Gemini: {e}"
                return JsonResponse({'success': False, 'error': error_message})
        else:
            return JsonResponse({'success': False, 'error': 'La query non può essere vuota.'})
    else:
        return JsonResponse({'success': False, 'error': 'Metodo non consentito.'}, status=405)


@staff_member_required
def get_adventure_summary_ajax(request):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        gemma = GemmaIstruction.objects.active()

        contents_for_gemini = []

        # Passa le istruzioni di sistema
        contents_for_gemini.append(gemma.system_instruction)

        # Ottieni solo gli ultimi N messaggi per limitare la cronologia e non saturare il contesto
        chat_messages = ChatMessage.objects.filter(author=request.user).order_by('-created_at')[:100]
        # Inverti l'ordine per avere i messaggi più vecchi prima
        for m in reversed(chat_messages):
            contents_for_gemini.append(f'Messaggio utente: {m.user_message}')
            contents_for_gemini.append(f'Risposta del sistema: {m.bot_response}')

        # Aggiungi i file ingestiti come contesto
        for f_gemini in client.files.list():
            contents_for_gemini.append(f_gemini)

        gemma = GemmaIstruction.objects.active()

        contents_for_gemini.append(
            gemma.summary_istruction,
        )

        if chat_messages:
            summary = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=contents_for_gemini,
            )
            summary_text = summary.text
        else:
            summary_text = ''

        # Restituisci la risposta come JSON
        return JsonResponse({
            'success': True, 
            'summary': markdown.markdown(summary_text),
        })

    except Exception as e:
        error_message = f"Errore durante la generazione della risposta da Gemini: {e}"
        return JsonResponse({'success': False, 'error': error_message})


@staff_member_required
def get_char_sheet_ajax(request):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        gemma = GemmaIstruction.objects.active()

        contents_for_gemini = []

        # Passa le istruzioni di sistema
        contents_for_gemini.append(gemma.system_instruction)

        # Ottieni solo gli ultimi N messaggi per limitare la cronologia e non saturare il contesto
        chat_messages = ChatMessage.objects.filter(author=request.user).order_by('-created_at')[:100]
        # Inverti l'ordine per avere i messaggi più vecchi prima
        for m in reversed(chat_messages):
            contents_for_gemini.append(f'Messaggio utente: {m.user_message}')
            contents_for_gemini.append(f'Risposta del sistema: {m.bot_response}')

        # Aggiungi i file ingestiti come contesto
        for f_gemini in client.files.list():
            contents_for_gemini.append(f_gemini)

        contents_for_gemini.append(
            gemma.character_sheet_istruction,
        )        

        if chat_messages:
            character_sheet = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=contents_for_gemini,
            )
            character_sheet_text = character_sheet.text
        else:
            character_sheet_text = ''

        # Restituisci la risposta come JSON
        return JsonResponse({
            'success': True, 
            'character_sheet': markdown.markdown(character_sheet_text),
        })

    except Exception as e:
        error_message = f"Errore durante la generazione della risposta da Gemini: {e}"
        return JsonResponse({'success': False, 'error': error_message})
