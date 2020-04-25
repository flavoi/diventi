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

    # Get the list of adventures that are 
    # related to products users have in their collection.
    def user_adventures(self):
        user = CuserMiddleware.get_user()
        try:
            if user.is_staff:
                products = Product.objects.user_authored(user)
            else:
                products = Product.objects.user_collection(user)
            return self.filter(product__in=products)
        except AttributeError:
            return self

    # Get the list of first ring adventures that are 
    # related to products users have in their collection.
    def first_rings(self):
        adventures = self.user_adventures()
        adventures = adventures.filter(ring='first')
        return adventures

    # Get a random second ring adventure that is 
    # related to products users have in their collection.
    # We can exclude adventures that have already been player.
    def random_second_ring(self, exclude_ids=None):
        adventure = self.user_adventures()
        adventure = adventure.filter(ring='second')
        if exclude_ids:
            adventure = adventure.exclude(pk__in=exclude_ids)
        adventure = adventure.order_by('?').first()
        return adventure

    # Returns the third ring of the adventure that is 
    # related to products users have in their collection.
    def third_ring(self):
        adventure = self.user_adventures()
        adventure = adventure.filter(ring='third')
        if adventure:
            adventure = adventure.get()
        else:
            adventure = adventure.none()
        return adventure


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
        ('first', _('First Ring')),
        ('second', _('Second Ring')),
        ('third', _('Third Ring')),
    ]
    ring = models.CharField(
        max_length=20, 
        choices=RING_CHOICES, 
        verbose_name=_('ring of storytelling'),
        help_text=_('Any adventure should have at least one ring of each type.')
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

    # Return game master's situations
    def history(self, game_master):
        situations = Situation.objects.filter(game_master=game_master)
        situations = situations.prefetch()
        return situations

    # Returns game master's situations that are yet to be resolved
    def open(self, game_master):
        situations = self.history(game_master)
        situations = situations.filter(resolution__isnull=True)
        return situations

    # Return third rings situations that the game master have played and resolved.
    def resolved(self, game_master):
        situations = self.filter(game_master=game_master)
        situations = situations.filter(adventure__ring='third')
        situations = situations.filter(resolution__isnull=False)
        return situations

    # Get the last situation of the story selecting by its uuid
    def current(self, uuid):
        situation = Situation.objects.filter(story=uuid).last()
        return situation


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
        related_name=_('situations'),
        verbose_name=_('story'),
    )

    objects = SituationQuerySet.as_manager()

    class Meta:
        verbose_name = _('Situation')
        verbose_name_plural = _('Situations')

    def __str__(self):
        return _('Situation n. %(pk)s') % {'pk': self.pk}

    def get_absolute_url(self):
        return reverse('adventures:situation_story_detail', args=[self.story.uuid,])

    def story_tag(self):
        if self.story:
            return mark_safe('<a href="{0}">{1}</a>'.format(self.story.get_absolute_url(), self.story.__str__()))
        else:
            return '-'
    story_tag.short_description = _('Story')