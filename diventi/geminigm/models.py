from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

from diventi.products.models import Product


class IngestedDocument(models.Model):
    title = models.CharField(
        max_length=255, 
        verbose_name=_('title')
    )
    source_url = models.URLField(
        max_length=2000, 
        null=True, 
        blank=True,
        verbose_name=_('source url')
    )
    file_path = models.CharField(
        max_length=1000, 
        null=True, 
        blank=True,
        verbose_name=_('file path'),
    )
    gemini_file_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        verbose_name=_('ID file Gemini'),
    )
    ingested_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('ingestion date'),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('ingested document')
        verbose_name_plural = _('ingested documents')


class GemmaIstructionQuerySet(models.QuerySet):

    # Returns the latest gemma that has active status
    def active(self):
        gemma = self.order_by('created_at')
        gemma = gemma.filter(active=True)
        return gemma

    # Fetch the product related to the gemma
    def product(self):
        gemma = self.select_related('gemma_product')
        return gemma

    def playable(self, user):
        gemma = self.active().product()
        gemma_public = gemma.filter(gemma_product__public=True)
        gemma_playtest = gemma.none()
        if user.has_perm('accounts.can_playtest'):
            gemma_playtest = gemma.filter(gemma_product__playtest_material=True)
        gemma = gemma_public | gemma_playtest
        return gemma


GEMMA = _("Sei un game master (GM) che deve gestire un gioco di ruolo da tavolo con ambientazione e meccaniche personalizzate denominato Primo Contatto (che trovi in allegato).  Tratta la conversazione come una sessione di gioco continua, ricordandoti tutti i dettagli che andranno via via emergendo. Tu genererai e descriverai (in maniera concisa ma evocativa) il mondo, gli eventi e gli esiti delle azioni di Personaggi Giocanti (PG) e Personaggi Non Giocanti (PNG). Deciderai anche come i PNG agiranno. Questa chat dovrà essere inclusa nel tuo contesto per generare le risposte, per cui dovrai ricordarti esattamente gli eventi che andranno verificandosi e i nomi/descrizioni dei luoghi e dei personaggi. Alcune note per il GM: rimani sempre in gioco come GM del gioco di ruolo, tu sei in controllo e sei responsabile di come il gioco evolverà. Cerca di mantenere le risposte concise e chiare. Evidenzia nomi, luoghi, oggetti. Le decisioni prese dovrebbero avere conseguenze e peso. Fornisci frequenti spunti narrativi per i giocatori e suggerisci possibili azioni che i personaggi potrebbero intraprendere. Usa creatività e varietà quando generi dei nomi di cose o persone. Non generarne di troppo simili. Il tema: la campagna è ambientata nel mondo di Primo Contatto, un pianeta Terra alternativo in cui nell'anno 2020 è caduto un oggetto celeste in Sud America, disattivando in tutte le Americhe la tecnologia come la conosciamo oggi. In quel giorno fatidico alcune persone hanno visto nascere dei poteri magici dentro di loro, chiamati doti. Rispetto delle regole: Segui scrupolosamente le regole del manuale che ti è stato fornito, con le seguenti eccezioni e adattamenti specifici che abbiamo stabilito durante la sessione: Improvvisazione: In caso di domande o azioni non previste dal manuale, improvvisa risposte che si allineino al tono e al tema del gioco. Evitare il metagioco: Non rivelare statistiche esatte di nemici o esiti di prove. Descrivi gli eventi in modo narrativo, lasciando che i giocatori scoprano i dettagli. Azione Combinata: Per un'azione combinata, ogni giocatore deve superare la propria prova; se un giocatore ha un successo eccezionale, può compensare un risultato inferiore di un altro, a discrezione del GM.")

SUMMARY_INSTRUCTION = _("Fai il riassunto degli avvenimenti più importanti avvenuti nell'avventura che l'utente sta giocando. Massimo due paragrafi discorsivi. Evita frasi introduttive come 'ok, ho capito', o 'va bene', o similari; scrivi direttamente il contenuto del riassunto. Se non ci sono eventi da riassumere, dì semplicemente che non hai informazioni e consiglia al giocatore di cominciare un'avventura con il GM.")

CHARACTER_SHEET_ISTRUCTION = _("Riporta le caratteristiche del personaggio che l'utente sta interpretando nell'avventura in un elenco puntato ordinato. Quando riporti una dote scrivi il nome in grassetto, l'effetto in modalità libera e quello in modalità a turni e infine l'elenco degli elementi che la compongono (flussi, poteri, attrezzi). Descrivi brevemente l'effetto dei sottosistemi della MTM. Riporta le relazioni per ultime e descrivile in un breve paragrafo. Difesa, punti vita e iperio potrebbero stare in un'unica riga. Non riportare frasi introduttive come 'ecco le caratteristiche, 'certamente' oppure 'ok rispondo', riporta direttamente il contenuto della risposta.")

WELCOME_MESSAGE_ISTRUCTION = _("Mostra un breve messaggio di benvenuto con un riepilogo del gioco. Massimo due paragrafi. Non rispondere 'Certamente', oppure 'ho capito', riporta direttamente la risposta.")

class GemmaIstruction(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name=_('title'),
    )
    short_description = models.TextField(
        blank=True, 
        max_length=50, 
        verbose_name=_('short description')
    )
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('slug'),
    )
    system_instruction = models.TextField(
        verbose_name=_('system istruction'),
    )
    summary_istruction = models.TextField(
        verbose_name=_('summary istruction'),
    )
    character_sheet_istruction = models.TextField(
        verbose_name=_('character sheet istruction'),
    )
    welcome_message_istruction = models.TextField(
        verbose_name=_('welcome message istruction')
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_('active'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation date'),
    )
    gemma_product = models.OneToOneField(
        Product, 
        null = True, 
        blank = True, 
        related_name = 'gemma', 
        on_delete = models.SET_NULL, 
        verbose_name = _('product'),
    )

    objects = GemmaIstructionQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('geminigm:gemma_private', args=[self.slug,])

    class Meta:
        verbose_name = _('Gemma istruction')
        verbose_name_plural = _('Gemma istructions')


class WelcomeMessage(models.Model):
    bot_response = models.TextField(
        verbose_name=_('bot response'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation date'),
    )
    gemma = models.ForeignKey(
        GemmaIstruction, 
        null = True, 
        related_name = 'welcome_messages', 
        verbose_name = _('gemma'), 
        on_delete = models.SET_NULL,
    )

    def __str__(self):
        return self.bot_response

    class Meta:
        verbose_name = _('Welcome message')
        verbose_name_plural = _('Welcome messages')



class ChatMessage(models.Model):
    user_message = models.TextField(
        verbose_name=_('user message'),
    )
    bot_response = models.TextField(
        verbose_name=_('bot response'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        verbose_name=_('author'),
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation date'),
    )
    gemma = models.ForeignKey(
        GemmaIstruction, 
        null = True, 
        related_name = 'chat_messages', 
        verbose_name = _('gemma'), 
        on_delete = models.SET_NULL,
    )

    def __str__(self):
        return self.user_message

    class Meta:
        verbose_name = _('chat message')
        verbose_name_plural = _('chat messages')
