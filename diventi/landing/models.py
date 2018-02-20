from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from cuser.middleware import CuserMiddleware

from diventi.core.models import Element, DiventiImageModel


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


class FeedbackManager(models.Manager):

    def usercount(self):        
        current_user = CuserMiddleware.get_user()
        feedbacks = 0
        if not current_user.is_anonymous: 
            feedbacks = self.filter(user=current_user)
            feedbacks = feedbacks.count()
        return feedbacks


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    description = models.TextField()

    objects = FeedbackManager()

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.user = CuserMiddleware.get_user()
        super(Feedback, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('feedback')
        verbose_name_plural = _('feedback')
        

class PresentationCover(DiventiImageModel):
    """
        Stores cover images for the features section.
    """
    DESCRIPTION = 'DES'
    FEATURES = 'FEA'
    SECTION_CHOICES = (
        (DESCRIPTION, 'description'),
        (FEATURES, 'features'), 
    )
    section = models.CharField(choices=SECTION_CHOICES, default=DESCRIPTION, max_length=3, verbose_name=_('section'))
    active = models.BooleanField(default=False, verbose_name=_('active'))

    class Meta:
        verbose_name = _('Presentation Cover')
        verbose_name_plural = _('Presentation Covers')


class Presentation(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    abstract = models.TextField(blank=True, verbose_name=_('abstract'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    cover = models.ImageField(blank=True, upload_to='landing/', verbose_name=_('cover'))
    presentation_covers = models.ForeignKey(PresentationCover, null=True, blank=True, verbose_name=_('presentation cover'))
    active = models.BooleanField(default=False, verbose_name=_('active'))
    

    objects = PresentationManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('presentation')
        verbose_name_plural = _('presentations')


class Feature(Element):    
    profile = models.ForeignKey(Presentation, related_name='features')

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')