from django.db import models
from django.conf import settings
from django.utils.html import mark_safe

from cuser.middleware import CuserMiddleware
from ckeditor.fields import RichTextField


COLORS_CHOICES = (
    ('info', 'Blue'),
    ('primary', 'Rose'),
    ('danger', 'Red'),
    ('success', 'Green'),
    ('default', 'Gray'),
)


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` field.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PromotableModel(models.Model):
    """
    An abstract base class model that enables a promotion feature
    similar to a facebook like on any model.
    """
    promotions = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def user_has_promoted(self):
        # Fetch the logged user thanks to a dedicated middleware
        user = CuserMiddleware.get_user() 
        if user in self.promotions.all():
            return True
        else:
            return False

    class Meta:
        abstract = True


class Element(models.Model):
    """
    An abstract base class model that represents a single piece of content of 
    any section.
    """
    icon = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    description = RichTextField()
    color = models.CharField(choices=COLORS_CHOICES, max_length=30, default='default')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class DiventiImageModel(models.Model):
    """
    An abstract base class that manages models based on images uploaded on Imgur.
    """
    image = models.URLField()
    label = models.CharField(max_length=50, blank=True)
    
    def image_thumbnail(self):
        # imgur legend
        # 't' stands for 'small thumbnail'
        # 's' stands for 'small square'
        IMAGE_MODE = 't'
        original_image = self.image
        image = original_image.replace('.png', '{0}.png'.format(IMAGE_MODE))
        if image == original_image:
            image = self.image.replace('.jpg', '{0}.jpg'.format(IMAGE_MODE))        
        return image

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{0}" />'.format(self.image_thumbnail()))
        else:
            return u'(Nessuna immagine)'    
    image_tag.short_description = 'Image'

    class Meta:
        abstract = True

    def __str__(self):
        return u'{0}'.format(self.label)

