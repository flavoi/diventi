import os, markdown, json
from google import genai
from google.genai import types

from django.shortcuts import (
    redirect, 
    render,
    get_object_or_404,
)
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import (
    gettext_lazy as _,
    get_language,
)
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin,
)

from diventi.accounts.utils import can_playtest
from diventi.products.models import Product

from .models import (
    ChatMessage,
    IngestedDocument,
    WelcomeMessage,
    GemmaIstruction,
    SectionAddon,
)
from .forms import PDFUploadForm, WebIngestionForm
from .utils import (
    ingest_pdf_document, 
    ingest_website_document,
    user_has_access_to_ai,
)


@require_POST
def generate_astral_description_ajax(request, section_addon_slug):
    """
    Riceve i dettagli del compagno astrale (nome, colore, specie, personalità, capacità),
    recupera le istruzioni da GemmaIstruction e invoca Gemini per elaborare
    una descrizione in linguaggio naturale fluida e narrativa.
    """
    name = request.POST.get('name', '').strip()
    colore = request.POST.get('colore', '').strip()
    specie = request.POST.get('specie', '').strip()
    personalita = request.POST.get('personalita', '').strip()
    capacita = request.POST.get('capacita', '').strip()

    if not (colore and specie and personalita):
        return JsonResponse(
            {'success': False, 'error': 'Parametri insufficienti per manifestare l\'astrale.'}, 
            status=400
        )

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # 1. Recupera la Sezione e le relative istruzioni Gemma
        section_addon = get_object_or_404(SectionAddon, slug=section_addon_slug)

        if not section_addon.enable_ai or not section_addon.gemma:
            raise Exception('Funzionalità IA non abilitata o istruzione Gemma non associata.')

        base_instruction = section_addon.gemma.system_instruction

        # 2. Costruzione del Prompt
        prompt = f"""
        {base_instruction}

        Dati del compagno astrale scelti dall'utente:
        - Nome: {name or 'Senza nome'}
        - Veste visiva / Colore: {colore}
        - Specie / Forma: {specie}
        - Personalità / Aspetto: {personalita}
        - Capacità speciale: {capacita}

        Genera un output in formato JSON valido con una singola chiave:
        "description": Una frase o breve paragrafo narrativo (massimo 45 parole) in linguaggio naturale che descriva in modo scorrevole, evocativo e coeso l'aspetto visivo e il comportamento del compagno astrale quando si manifesta.

        Rispondi ESCLUSIVAMENTE con un oggetto JSON valido. Non includere blocchi di codice markdown o testo aggiuntivo.
        """

        # 3. Gestione multilingua
        lan = get_language()
        if lan == 'en':
            prompt += " Genera il valore del campo 'description' direttamente in lingua inglese."
        else:
            prompt += " Genera il valore del campo 'description' in lingua italiana."

        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
        )

        # 4. Parsing sicuro del JSON
        raw_text = response.text.strip()
        if raw_text.startswith('```'):
            raw_text = raw_text.split('\n', 1)[-1]
            if raw_text.endswith('```'):
                raw_text = raw_text.rsplit('\n', 1)[0]
            raw_text = raw_text.replace('```json', '').replace('```', '').strip()

        data = json.loads(raw_text)

        return JsonResponse({
            'success': True,
            'description': data.get('description', '')
        })

    except Exception as e:
        print("\n" + "="*50)
        print(" [DEBUG ASTRAL AI ERROR] ")
        traceback.print_exc()
        print("="*50 + "\n")

        return JsonResponse(
            {'success': False, 'error': f"Errore durante l'elaborazione dell'Astrale: {str(e)}"}, 
            status=500
        )
        

@require_POST
def generate_spell_name_ajax(request, section_addon_slug):
    """
    Riceve le parole dell'Arcanum via POST (forma, fonte, portata),
    recupera le istruzioni di sistema dal modello GemmaIstruction collegato alla Sezione
    e invoca Gemini per generare nome e descrizione.
    """
    forma = request.POST.get('forma', '').strip()
    fonte = request.POST.get('fonte', '').strip()
    portata = request.POST.get('portata', '').strip()

    if not (forma and fonte and portata):
        return JsonResponse(
            {'success': False, 'error': 'Tutti e tre i componenti magici sono obbligatori.'}, 
            status=400
        )

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # 1. Recupera la Sezione
        section_addon = get_object_or_404(SectionAddon, slug=section_addon_slug)

        if not section_addon.enable_ai:
            raise Exception(f'Abilitare la funzionalità IA per questo addon: {section_addon}')

        # 2. Controllo di sicurezza: verifica che l'addon abbia una Gemma assegnata
        if not section_addon.gemma:
            raise Exception(f'Nessuna istruzione Gemma (GemmaIstruction) associata a questo addon dall\'Admin: {section_addon}')

        # 2. Costruisci il prompt combinando le istruzioni da DB con i dati dinamici scelti dall'utente
        base_instruction = section_addon.gemma.system_instruction
        
        prompt = f"""
        {base_instruction}

        Componenti selezionati dall'utente:
        - Forma: {forma}
        - Fonte: {fonte}
        - Portata: {portata}

        Genera un output in formato JSON valido con esattamente due chiavi:
        1. "name": Un nome unico, epico ed evocativo per l'incantesimo.
        2. "description": Una breve frase narrativa (massimo 25 parole) che descriva l'effetto visivo quando viene invocato.

        Rispondi ESCLUSIVAMENTE con un oggetto JSON valido. Non includere blocchi di codice markdown.
        """

        # 3. Gestione multilingua
        lan = get_language()
        if lan == 'en':
            prompt += " Genera sia il campo 'name' che 'description' direttamente in lingua inglese. Non riportare frasi introduttive o finali, limitati a restituire il JSON con i valori tradotti."
        
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
        )

        # 4. Parsing sicuro della risposta JSON
        raw_text = response.text.strip()
        if raw_text.startswith('```'):
            raw_text = raw_text.split('\n', 1)[-1]
            if raw_text.endswith('```'):
                raw_text = raw_text.rsplit('\n', 1)[0]
            raw_text = raw_text.replace('```json', '').replace('```', '').strip()

        data = json.loads(raw_text)

        return JsonResponse({
            'success': True,
            'name': data.get('name', f"{forma} di {fonte}"),
            'description': data.get('description', '')
        })

    except Exception as e:
        # STAMPA IL TRACEBACK COMPLETO NEL TERMINALE DI RUNSERVER
        print("\n" + "="*50)
        print(" [DEBUG AJAX ERROR] ")
        traceback.print_exc()
        print("="*50 + "\n")

        return JsonResponse(
            {'success': False, 'error': "Errore durante l'evocazione dell'Arcanum: %(error)s" % {'error': str(e)}}, 
            status=500
        )


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


class UserHasProductMixin(UserPassesTestMixin):
    """ 
        This view checks if the user has bought the product
        related to the requested gemma. 
        It assumes to have the slug of the book object available
        in gemma_slug get parameter.
    """

    permission_denied_message = _('This game is not in your collection, please check your profile.')

    def test_func(self):
        gemma_slug = self.kwargs.get('gemma_slug', None)
        gemma = get_object_or_404(GemmaIstruction, slug=gemma_slug)
        product = gemma.gemma_product
        user_has_access = user_has_access_to_ai(product=product, user=self.request.user)
        if not user_has_access:
            self.permission_denied_message = _('This game is not in your collection, please check your profile.')        
        return user_has_access 


class PublicGemmaMixin(UserPassesTestMixin):
    """
        Returns the gemma if the product is public, or else it redirects to the default view.
    """
    def test_func(self):
        gemma_slug = self.kwargs.get('gemma_slug', None)
        gemma = get_object_or_404(GemmaIstruction, slug=gemma_slug)
        product = get_object_or_404(Product, id=gemma.gemma_product.id)
        gemma_is_public_test = product.public
        if not gemma_is_public_test:
            self.permission_denied_message = _("This gemma has no content attached, please contact the authors.")
        return gemma_is_public_test


class GemmaDetailView(DetailView):
    """ Returns the gemma. """
    
    model = GemmaIstruction
    slug_url_kwarg = 'gemma_slug'
    template_name = 'geminigm/gemma_detail.html'
    context_object_name = 'gemma'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.active().product()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bought'] = self.object.gemma_product.user_has_already_bought(self.request.user)
        welcome_message = ""
        try:
            welcome_message = WelcomeMessage.objects.filter(gemma=self.object.id).latest('created_at').bot_response
        except WelcomeMessage.DoesNotExist:
            welcome_message = _("Welcome to your Primo Contatto adventure!")
        context['welcome_message'] = markdown.markdown(welcome_message)
        return context


class PublicGemmaView(PublicGemmaMixin, GemmaDetailView):
    """
        Renders the gemma regardless of the user or their collection.
    """
    pass


class PrivateGemmaView(LoginRequiredMixin, UserHasProductMixin, GemmaDetailView):
    """
        Renders the gemma if and only if the user is authenticated 
        and has the product in their collection.
    """
    pass


def chatbot_view(request, gemma_slug=None):
    welcome_message = ""
    try:
        welcome_message = WelcomeMessage.objects.latest('created_at').bot_response
    except WelcomeMessage.DoesNotExist:
        welcome_message = "Benvenuto nella tua avventura di Primo Contatto!"

    context = {
        'welcome_message': markdown.markdown(welcome_message),
    }
    return render(request, 'geminigm/chatbot.html', context)


def send_message_ajax(request, gemma_slug):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        gemma = get_object_or_404(GemmaIstruction, slug=gemma_slug)
        product = gemma.gemma_product
        user_has_access = user_has_access_to_ai(product=product, user=request.user)

        if query and user_has_access:
            try:
                client = genai.Client(api_key=settings.GEMINI_API_KEY)

                contents_for_gemini = []

                # Passa le istruzioni di sistema
                contents_for_gemini.append(gemma.system_instruction)

                # Ottieni solo gli ultimi N messaggi per limitare la cronologia e non saturare il contesto
                chat_messages = ChatMessage.objects.history(gemma=gemma)
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
                    model='gemini-3-flash-preview',
                    contents=contents_for_gemini,
                )
                response_text = response.text

                lan = get_language()
                if lan == 'en':
                    response = client.models.generate_content(
                        model='gemini-3-flash-preview',
                        contents=f'traduci in inglese {response_text}. Non riportare frasi introduttive o finali, limitati a resistuire la traduzione.',
                    )
                    response_text = response.text
                ChatMessage.objects.create(user_message=query, bot_response=response_text, author=request.user, gemma=gemma)

                return JsonResponse({
                    'success': True, 
                    'bot_response': markdown.markdown(response_text),
                })

            except Exception as e:
                error_message = f"Errore durante la generazione della risposta da Gemini: {e}"
                return JsonResponse({'success': False, 'error': error_message})
        else:
            return JsonResponse({'success': False, 'error': 'La query non può essere vuota e l\'utente deve essere abilitato.'})
    else:
        return JsonResponse({'success': False, 'error': 'Metodo non consentito.'}, status=405)


def get_adventure_summary_ajax(request, gemma_slug):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        gemma = get_object_or_404(GemmaIstruction, slug=gemma_slug)
        product = gemma.gemma_product
        user_has_access = user_has_access_to_ai(product=product, user=request.user)

        if user_has_access:
            contents_for_gemini = []

            # Passa le istruzioni di sistema
            contents_for_gemini.append(gemma.system_instruction)

            # Ottieni solo gli ultimi N messaggi per limitare la cronologia e non saturare il contesto
            chat_messages = ChatMessage.objects.history(gemma=gemma)
            # Inverti l'ordine per avere i messaggi più vecchi prima
            for m in reversed(chat_messages):
                contents_for_gemini.append(f'Messaggio utente: {m.user_message}')
                contents_for_gemini.append(f'Risposta del sistema: {m.bot_response}')

            # Aggiungi i file ingestiti come contesto
            for f_gemini in client.files.list():
                contents_for_gemini.append(f_gemini)

            contents_for_gemini.append(
                gemma.summary_istruction,
            )
            
            if chat_messages:
                summary = client.models.generate_content(
                    model='gemini-3-flash-preview',
                    contents=contents_for_gemini,
                )
                summary_text = summary.text
            else:        
                summary_text = ''

            return JsonResponse({
                'success': True, 
                'summary': markdown.markdown(summary_text),
            })
        else:
            raise Exception
        
    except Exception as e:
        error_message = f"Errore durante la generazione della risposta da Gemini: {e}"
        return JsonResponse({'success': False, 'error': error_message})


def get_char_sheet_ajax(request, gemma_slug):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        gemma = get_object_or_404(GemmaIstruction, slug=gemma_slug)
        product = gemma.gemma_product
        user_has_access = user_has_access_to_ai(product=product, user=request.user)

        if user_has_access:
            contents_for_gemini = []

            # Passa le istruzioni di sistema
            contents_for_gemini.append(gemma.system_instruction)

            # Ottieni solo gli ultimi N messaggi per limitare la cronologia e non saturare il contesto
            chat_messages = ChatMessage.objects.history(gemma=gemma)

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
                    model='gemini-3-flash-preview',
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
        
        else:
            raise Exception

    except Exception as e:
        error_message = f"Errore durante la generazione della risposta da Gemini: {e}"
        return JsonResponse({'success': False, 'error': error_message})
