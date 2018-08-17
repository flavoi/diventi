from django.db import models
from django.utils.translation import gettext_lazy as _

from diventi.core.models import TimeStampedModel, PublishableModel, DiventiImageModel


class Brew(TimeStampedModel):
    """
        A brew is fantastic document written in latex that contains
        our juicy adventures.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    description = models.TextField(max_length=250, verbose_name=_('description'))
    content = models.TextField(verbose_name=_('content'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('brew')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('homebrew:detail', args=[str(self.slug)])
