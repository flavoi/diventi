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
)
from .forms import PDFUploadForm, WebIngestionForm
from .utils import (
    ingest_pdf_document, 
    ingest_website_document,
    user_has_access_to_ai,
)


HISTORY_DEPTH = 85

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
                chat_messages = ChatMessage.objects.filter(author=request.user).order_by('-created_at')[:HISTORY_DEPTH]
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

                lan = get_language()
                if lan == 'en':
                    response = client.models.generate_content(
                        model='gemini-2.5-flash-lite',
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
            chat_messages = ChatMessage.objects.filter(author=request.user).order_by('-created_at')[:HISTORY_DEPTH]
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
                    model='gemini-2.5-flash-lite',
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
            chat_messages = ChatMessage.objects.filter(author=request.user).order_by('-created_at')[:HISTORY_DEPTH]
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
        
        else:
            raise Exception

    except Exception as e:
        error_message = f"Errore durante la generazione della risposta da Gemini: {e}"
        return JsonResponse({'success': False, 'error': error_message})
