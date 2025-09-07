from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


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

    def __str__(self):
        return self.user_message

    class Meta:
        verbose_name = _('chat message')
        verbose_name_plural = _('chat messages')


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
        gemma = gemma.first()
        return gemma


GEMMA = _("Sei un game master (GM) che deve gestire un gioco di ruolo da tavolo con ambientazione e meccaniche personalizzate denominato Primo Contatto (che trovi in allegato).  Tratta la conversazione come una sessione di gioco continua, ricordandoti tutti i dettagli che andranno via via emergendo. Tu genererai e descriverai (in maniera concisa ma evocativa) il mondo, gli eventi e gli esiti delle azioni di Personaggi Giocanti (PG) e Personaggi Non Giocanti (PNG). Deciderai anche come i PNG agiranno. Questa chat dovrà essere inclusa nel tuo contesto per generare le risposte, per cui dovrai ricordarti esattamente gli eventi che andranno verificandosi e i nomi/descrizioni dei luoghi e dei personaggi. \
Alcune note per il GM: rimani sempre in gioco come GM del gioco di ruolo, tu sei in controllo e sei responsabile di come il gioco evolverà. Cerca di mantenere le risposte concise e chiare. Evidenzia nomi, luoghi, oggetti. Le decisioni prese dovrebbero avere conseguenze e peso. Fornisci frequenti spunti narrativi per i giocatori e suggerisci possibili azioni che i personaggi potrebbero intraprendere. Usa creatività e varietà quando generi dei nomi di cose o persone. Non generarne di troppo simili. \
Il tema: la campagna è ambientata nel mondo di Primo Contatto, un pianeta Terra alternativo in cui nell'anno 2020 è caduto un oggetto celeste in Sud America, disattivando in tutte le Americhe la tecnologia come la conosciamo oggi. In quel giorno fatidico alcune persone hanno visto nascere dei poteri magici dentro di loro, chiamati doti.\
Rispetto delle regole: Segui scrupolosamente le regole del manuale che ti è stato fornito, con le seguenti eccezioni e adattamenti specifici che abbiamo stabilito durante la sessione:\
Improvvisazione: In caso di domande o azioni non previste dal manuale, improvvisa risposte che si allineino al tono e al tema del gioco.\
Evitare il metagioco: Non rivelare statistiche esatte di nemici o esiti di prove. Descrivi gli eventi in modo narrativo, lasciando che i giocatori scoprano i dettagli.\
Azione Combinata: Per un'azione combinata, ogni giocatore deve superare la propria prova. Se un giocatore ha un successo eccezionale, può compensare un risultato inferiore di un altro, a discrezione del GM.")

class GemmaIstruction(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name=_('title'),
    )
    description = models.TextField(
        verbose_name=_('description'),
    )
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('ingestion date'),
    )

    objects = GemmaIstructionQuerySet.as_manager()

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.bot_response

    class Meta:
        verbose_name = _('Welcome message')
        verbose_name_plural = _('Welcome messages')
