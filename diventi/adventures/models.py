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


class Situation(TimeStampedModel):
    """An adventure instance that players can join."""
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Match', 
        blank=False,
        verbose_name=_('players')
    )
    
    class Meta:
        verbose_name = _('Situation')
        verbose_name_plural = _('Situations')

    def __str__(self):
        return _('Situation n. %(id)s') % {'id': self.id}

    def get_absolute_url(self):
        return reverse('adventures:situation_detail', args=[self.uuid,])


class Match(TimeStampedModel):
    situation = models.ForeignKey(
        Situation, 
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
        verbose_name=_('situation')
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


class StoryQuerySet(models.QuerySet):

    def prefetch(self):
        stories = self.select_related('adventure')
        stories = self.select_related('adventure__section')
        return stories

    # Returns the story if the game master is staff or the current user
    def game_master(self, user):
        if user.is_staff or user == self.game_master:
            story = self
        else:
            msg = _("This user is not the game master associated to this story.")
            raise self.model.DoesNotExist(msg)
        story = story.prefetch()
        return story

    # Return game master's stories and eventually exclude one from the list
    # We usually exclude the one that has recently been created 
    def stories(self, game_master, exclude_story=None):
        stories = Story.objects.filter(game_master=game_master)
        if exclude_story:
            stories = stories.exclude(pk=exclude_story.pk) 
        stories = stories.prefetch()
        return stories


class Resolution(Element):
    """ Represent the resolution of a story. """

    class Meta:
        verbose_name = _('Resolution')
        verbose_name_plural = _('Resolutions')

    def __str__(self):
        return _('%(title)s') % {'title': self.title}


class Story(TimeStampedModel):
    """An adventure instance hosted by a game master."""
    adventure = models.ForeignKey(
        Adventure,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name=_('stories'),
        verbose_name=_('adventure'),
    )
    game_master = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='stories', 
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
        related_name=_('stories'),
        verbose_name=_('resolution'),
    )
    next_story = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('next story'),
    )
    situation = models.ForeignKey(
        Situation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name=_('stories'),
        verbose_name=_('situation'),
    )

    objects = StoryQuerySet.as_manager()

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')

    def __str__(self):
        return _('Story n. %(id)s') % {'id': self.id}

    def get_absolute_url(self):
        return reverse('adventures:story_detail', args=[self.pk,])

    def situation_tag(self):
        if self.situation:
            return mark_safe('<a href="{0}">{1}</a>'.format(self.situation.get_absolute_url(), self.situation.__str__()))
        else:
            return '-'
    situation_tag.short_description = _('Situation')