from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from cuser.middleware import CuserMiddleware

from diventi.core.models import Element, DiventiImageModel, TimeStampedModel, DiventiCoverModel


class PresentationManager(models.Manager):

    def active(self):
        try:
            active_presentation = self.prefetch_related('features')
            active_presentation = self.prefetch_related('about')
            active_presentation = active_presentation.get(active=True)
        except Presentation.DoesNotExist:
            msg = _("There is no active landing page.")
            raise Presentation.DoesNotExist(msg)
        except Presentation.MultipleObjectsReturned:
            msg = _("There must be only one landing page at a time. Please fix!")
            raise Presentation.MultipleObjectsReturned(msg)
        return active_presentation


class Presentation(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    abstract = models.TextField(blank=True, verbose_name=_('abstract'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    cover = models.ImageField(blank=True, upload_to='landing/', verbose_name=_('cover'))
    active = models.BooleanField(default=False, verbose_name=_('active'))
    
    objects = PresentationManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('presentation')
        verbose_name_plural = _('presentations')


class About(models.Model):
    profile = models.ForeignKey(Presentation, null=True, related_name='about', on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('about')
        verbose_name_plural = _('about')


class Feature(Element):    
    profile = models.ForeignKey(Presentation, null=True, related_name='features', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')


class AboutCover(DiventiCoverModel):

    class Meta:
        verbose_name = _('About Cover')
        verbose_name_plural = _('About Covers')