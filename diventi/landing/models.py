from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from diventi.core.models import Element


class PresentationManager(models.Manager):

    def active(self):
        try:
            active_presentation = self.prefetch_related('features')
            active_presentation = active_presentation.get(active=True)
        except Presentation.DoesNotExist:
            msg = _("There is no active landing page.")
            raise Presentation.DoesNotExist(msg)
        except Presentation.MultipleObjectsReturned:
            msg = _("There must be only one landing page at a time. Please fix!")
            raise Presentation.MultipleObjectsReturned(msg)
        return active_presentation


class Presentation(models.Model):
    title = models.CharField(max_length=50)
    abstract = RichTextField(blank=True)
    description = RichTextField(blank=True)
    cover = models.ImageField(blank=True, upload_to='landing/')
    active = models.BooleanField(default=False, verbose_name=_('active'))

    objects = PresentationManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('presentation')
        verbose_name_plural = _('presentations')


class Feature(Element):    
    profile = models.ForeignKey(Presentation, related_name='features')