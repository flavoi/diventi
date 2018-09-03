from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.utils.html import mark_safe

from cuser.middleware import CuserMiddleware


COLORS_CHOICES = (
    ('info', _('Blue')),
    ('primary', _('Rose')),
    ('danger', _('Red')),
    ('warning', _('Yellow')),
    ('success', _('Green')),
    ('default', _('Gray')),
)


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` field.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """
    An abstract base class model that updates the publication
    date as soon as it becomes published.
    """
    published = models.BooleanField(default=False, verbose_name=_('published'))
    publication_date = models.DateTimeField(blank=True, null=True, verbose_name=_('publication_date'))

    # Pubblication date is updated if published has been modified from False to True
    def __init__(self, *args, **kwargs):
        super(PublishableModel, self).__init__(*args, **kwargs)
        self.old_published = self.published

    def save(self, *args, **kwargs):
        if self.old_published != self.published and self.published:
            self.publication_date = timezone.now()
        print(self.publication_date)
        super(PublishableModel, self).save(*args, **kwargs)


class PromotableModel(models.Model):
    """
    An abstract base class model that enables a promotion feature
    similar to a facebook like on any model.
    """
    promotions = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name=_('promotions'))

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
    icon = models.CharField(max_length=30, verbose_name=_('icon'))
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    color = models.CharField(choices=COLORS_CHOICES, max_length=30, default='default', verbose_name=_('color'))

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Category(models.Model):
    """
    An abstract base class model that defines a specific type of an object.
    """
    title = models.CharField(max_length=60, unique=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("categories")
        abstract = True


class DiventiImageModel(models.Model):
    """
    An abstract base class that manages models based on images uploaded on Imgur.
    """
    image = models.URLField(verbose_name=_('image'))
    label = models.CharField(max_length=50, blank=True, verbose_name=_('label'))
    
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
            return _('No image')    
    image_tag.short_description = _('Image')

    class Meta:
        abstract = True

    def __str__(self):
        return u'{0}'.format(self.label)


class DiventiCoverQuerySet(models.QuerySet):

    # Get the active cover or returns nothing
    def active(self):
        try:
            cover = self.model.objects.get(active=True)
        except self.model.DoesNotExist:
            cover = self.model.objects.none()
        except self.model.MultipleObjectsReturned:
            msg = _("There must be only one cover at a time. Please fix!")
            raise self.model.MultipleObjectsReturned(msg)
        return cover


class DiventiCoverManager(models.Manager):

    def get_queryset(self):
        return DiventiCoverQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class DiventiCoverModel(DiventiImageModel):
    """
        Stores cover images for the blog page.
    """

    active = models.BooleanField(default=False, verbose_name=_('active'))

    objects = DiventiCoverManager()

    class Meta:
        abstract = True
