from django.db import models

from ckeditor.fields import RichTextField


COLORS_CHOICES = (
    ('info', 'Blue'),
    ('primary', 'Rose'),
    ('danger', 'Red'),
    ('success', 'Green'),
    ('default', 'Gray'),       
)


class PresentationManager(models.Manager):

    def active(self):
        try:
            active_presentation = Presentation.objects.get(active=True)
        except Presentation.DoesNotExist:
            msg = "There is no active profile."
            raise Presentation.DoesNotExist(msg)
        except Presentation.MultipleObjectsReturned:
            msg = "There must be only one profile at a time. Please fix!"
            raise Presentation.MultipleObjectsReturned(msg)
        return active_presentation


class Presentation(models.Model):
    title = models.CharField(max_length=50)
    abstract = RichTextField(blank=True)
    description = RichTextField(blank=True)
    image = models.ImageField(blank=True, upload_to='landing/')
    paper_url = models.URLField(blank=True)
    active = models.BooleanField(default=False)

    objects = PresentationManager()

    def __str__(self):
        return self.title


class Feature(models.Model):
    icon = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    description = RichTextField()
    color = models.CharField(choices=COLORS_CHOICES, max_length=30, default='default')
    profile = models.ForeignKey(Presentation)

    def __str__(self):
        return self.title