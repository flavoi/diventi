from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

from diventi.core.models import (
    Element, 
    TimeStampedModel, 
    PublishableModel, 
    DisclosableModel, 
    DiventiImageModel, 
    DiventiColModel
)
from diventi.ebooks.models import Book


class CharacterSheet(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    origin = models.CharField(max_length=50, verbose_name=_('origin'))
    predisposition = models.CharField(max_length=50, verbose_name=_('predisposition'))
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('player'))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('book'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))

    def __str__(self):
        return '{0}'.format(self.name)

    def get_absolute_url(self):
        return reverse('sheets:charactersheet-detail', args=[self.slug, self.book.slug])

    class Meta:
        verbose_name = _('character sheet')
        verbose_name_plural = _('character sheets')


class Relationship(Element):
    character = models.ForeignKey(CharacterSheet, on_delete=models.CASCADE, verbose_name=('character'))

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
