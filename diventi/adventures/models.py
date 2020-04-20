import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import mark_safe

from cuser.middleware import CuserMiddleware

from diventi.core.models import (
    Element,
    TimeStampedModel,
)
from diventi.ebooks.models import (
    Section,
)
from diventi.products.models import (
    Product,
)


class AdventureQuerySet(models.QuerySet):

    # Get the list of firs ring adventures that are 
    # related to products users have in their collection.
    def first_rings(self):
        adventures = self.filter(ring='first')
        user = CuserMiddleware.get_user()
        try:
            if user.is_staff:
                products = Product.objects.user_authored(user)
            else:
                products = Product.objects.user_collection(user)
            adventures = adventures.filter(product__in=products)
        except AttributeError:
            pass
        return adventures


class Adventure(Element, TimeStampedModel):
    """A single piece of adventure."""
    section = models.ForeignKey(
        Section, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name=_('adventures'), 
        verbose_name=_('section'),
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name=_('adventures'),
        verbose_name=_('product'),
    ) 
    RING_CHOICES = [
        ('first', _('First')),
        ('second', _('Second')),
        ('third', _('Third')),
    ]
    ring = models.CharField(
        max_length=20, 
        choices=RING_CHOICES, 
        verbose_name=_('ring of storytelling'),
    )

    objects = AdventureQuerySet.as_manager()

    class Meta:
        verbose_name = _('Adventure')
        verbose_name_plural = _('Adventures')


class Story(TimeStampedModel):
    """An adventure instance that players can join."""
    uuid = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Match', 
        blank=False,
        verbose_name=_('players')
    )

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')

    def __str__(self):
        return _('Story n. %(uuid)s') % {'uuid': self.uuid}

    def get_absolute_url(self):
        return reverse('adventures:story_detail', args=[self.uuid,])


class Match(TimeStampedModel):
    story = models.ForeignKey(
        Story, 
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
        verbose_name=_('story')
    )
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
        verbose_name=_('customer')
    )

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')

    def __str__(self):
        return _('Match n. %(id)s') % {'id': self.id}


class Resolution(Element):
    """ Represent the resolution of a situation. """

    class Meta:
        verbose_name = _('Resolution')
        verbose_name_plural = _('Resolutions')

    def __str__(self):
        return _('%(title)s') % {'title': self.title}


class SituationQuerySet(models.QuerySet):

    def prefetch(self):
        situations = self.select_related('adventure')
        situations = self.select_related('adventure__section')
        situations = self.select_related('story')
        return situations

    # Returns the situation if the game master is staff or the current user
    def game_master(self, user):
        if user.is_staff or user == self.game_master:
            situation = self
        else:
            msg = _("This user is not the game master associated to this situation.")
            raise self.model.DoesNotExist(msg)
        situation = situation.prefetch()
        return situation

    # Return game master's situations and eventually exclude one from the list
    # We usually exclude the one that has recently been created 
    def gm_situations(self, game_master, exclude_situation=None):
        situations = Situation.objects.filter(game_master=game_master)
        if exclude_situation:
            situations = Situations.exclude(pk=exclude_situation.pk) 
        situations = situations.prefetch()
        return situations


class Situation(TimeStampedModel):
    """An adventure instance hosted by a game master."""
    adventure = models.ForeignKey(
        Adventure,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name=_('situations'),
        verbose_name=_('adventure'),
    )
    game_master = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='situations', 
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_('game master'),
    )
    resolution = models.ForeignKey(
        Resolution,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name=_('situations'),
        verbose_name=_('resolution'),
    )
    next_situation = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('next situation'),
    )
    story = models.ForeignKey(
        Story,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name=_('situation'),
        verbose_name=_('story'),
    )

    objects = SituationQuerySet.as_manager()

    class Meta:
        verbose_name = _('Situation')
        verbose_name_plural = _('Situations')

    def __str__(self):
        return _('Situation n. %(pk)s') % {'pk': self.pk}

    def get_absolute_url(self):
        return reverse('adventures:situation_detail', args=[self.story.uuid,])

    def story_tag(self):
        if self.story:
            return mark_safe('<a href="{0}">{1}</a>'.format(self.story.get_absolute_url(), self.story.__str__()))
        else:
            return '-'
    story_tag.short_description = _('Story')