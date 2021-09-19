import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.utils.html import mark_safe

from cuser.middleware import CuserMiddleware


COLORS_CHOICES = (
    ('info', _('Light blue')),
    ('primary', _('Blue')),
    ('danger', _('Red')),
    ('warning', _('Yellow')),
    ('success', _('Green')),
    ('secondary', _('Gray')),
    ('dark', _('Black')),
    ('light', _('White')),
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


class PublishableModelQuerySet(models.QuerySet):

    # Get the list of published objects
    def published(self):
        """
        We show every objects to staff as a preview
        even if they are not published, yet.
        """
        user = CuserMiddleware.get_user()
        qs = self
        if not user.is_staff:
            qs = qs.filter(published=True)
        return qs


class PublishableModelManager(models.Manager):

    def get_queryset(self):
        return PublishableModelQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class PublishableModel(models.Model):
    """
    A concrete base class model that updates the publication
    date as soon as it becomes published.
    """
    published = models.BooleanField(default=False, verbose_name=_('published'))
    publication_date = models.DateTimeField(blank=True, null=True, verbose_name=_('publication_date'))

    objects = PublishableModelManager()

    # Pubblication date is updated if published has been modified from False to True
    def __init__(self, *args, **kwargs):
        super(PublishableModel, self).__init__(*args, **kwargs)
        self.old_published = self.published

    def save(self, *args, **kwargs):
        if self.old_published != self.published and self.published:
            self.publication_date = timezone.now()
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
    An abstract base class model that represents a single piece of content.
    """
    title = models.CharField(
        max_length = 80,
        verbose_name = _('title'),
    )
    icon = models.CharField(
        blank = True,
        max_length = 30, 
        verbose_name = _('icon'),
    )
    ICON_STYLE_CHOICES = (
        ('r', 'r - regular'),
        ('s', 's - solid'),
        ('l', 'l - light'),
        ('d', 'd - duotone'),
        ('b', 'b - brand'),

    )
    ICON_STYLE_DEFAULT = 'r'
    icon_style = models.CharField(
        blank = True,
        choices = ICON_STYLE_CHOICES,
        default = ICON_STYLE_DEFAULT,
        max_length = 1,
        verbose_name = _('icon style')
    )
    description = models.TextField(blank=True, verbose_name=_('description'))
    color = models.CharField(blank=True, choices=COLORS_CHOICES, max_length=30, default='default', verbose_name=_('color'))

    def __str__(self):
        return self.title

    def icon_tag(self):
        if self.icon:
            return mark_safe('<i class="fa{0} fa-{1} fa-2x fa-fw"></i>'.format(self.icon_style, self.icon))
        else:
            return _('No icon')    
    icon_tag.short_description = _('Icon')

    def color_tag(self):
        if self.color:
            return mark_safe('<b class="text-{0}">{1}</b>'.format(self.color, self.get_color_display()))
        else:
            return _('No color')    
    color_tag.short_description = _('Color')

    class Meta:
        abstract = True


class Category(models.Model):
    """
    An abstract base class model that defines a specific type of object.
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
    An abstract base class that manages models based on images uploaded on the internet.
    """
    image = models.URLField(blank=True, verbose_name=_('image'))
    label = models.CharField(max_length=50, blank=True, verbose_name=_('label'))

    def image_tag(self):
        if self.image:
            return mark_safe('<img style="max-width:120px;" src="{0}" />'.format(self.image))
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
            msg = _("There must be only one object at a time. Please fix!")
            raise self.model.MultipleObjectsReturned(msg)
        return cover


class DiventiCoverManager(models.Manager):

    def get_queryset(self):
        return DiventiCoverQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class DiventiCoverModel(DiventiImageModel):
    """
    An abstract base class that helps to implement an image that can be activated.
    """

    active = models.BooleanField(default=False, verbose_name=_('active'))

    objects = DiventiCoverManager()

    class Meta:
        abstract = True


class FeaturedModelQuerySet(PublishableModelQuerySet):

    # Get the featured object that can be selected to appear on the landing page
    # Even super users should not see featured objects if they are not strictly published
    def featured(self):
        try:
            featured_model = self.published().get(featured=True)            
        except self.model.DoesNotExist:
            # Fail silently, return nothing
            featured_model = self.none() 
        except self.model.MultipleObjectsReturned:
            msg = _('Multiple featured objects returned. Please fix!')
            raise self.model.MultipleObjectsReturned(msg)  
        return featured_model

    # Get the not featured object that can be selected to appear on the landing page
    def not_featured(self):
        not_featured_models = self.published().filter(featured=False)
        return not_featured_models


class FeaturedModelManager(models.Manager):

    def get_queryset(self):
        return FeaturedModelQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured(self):
        return self.get_queryset().featured()

    def not_featured(self):
        return self.get_queryset().not_featured()


class FeaturedModel(PublishableModel):
    """
    An abstract base class that includes a featured boolean field
    
    """
    featured = models.BooleanField(default=False, verbose_name=_('featured'))

    objects = FeaturedModelManager()

    class Meta:
        abstract = True


class HighlightedModelQuerySet(models.QuerySet):

    # Get the highlighted object or the first item of the queryset
    def highlighted_or_first(self):
        try:
            highlighted_model = self.get(highlighted=True)            
        except self.model.DoesNotExist:
            # Fail silently and return the first item
            highlighted_model = self.first()
        except self.model.MultipleObjectsReturned:
            msg = _('Multiple highlighted objects returned. Please fix!')
            raise self.model.MultipleObjectsReturned(msg)  
        return highlighted_model


class HighlightedModelManager(models.Manager):

    def get_queryset(self):
        return HighlightedModelQuerySet(self.model, using=self._db)

    def highlighted_or_first(self):
        return self.get_queryset().highlighted_or_first()    


class HighlightedModel(models.Model):
    """
        An abstract bae class that includes a featured boolean field
        without the publishable functionality.
    """
    highlighted = models.BooleanField(default=False, verbose_name=_('highlighted'))

    objects = HighlightedModelManager()

    class Meta:
        abstract = True


class DiventiColModel(models.Model):
    COL_CHOICES = [
        (12, _('Full (12)')),
        (8, _('Two thirds (8)')),
        (6, _('Half (6)')),
        (4, _('One third (4)')),
        (3, _('One fourth (3)')),
    ]
    col_lg = models.PositiveIntegerField(default=12, choices=COL_CHOICES, verbose_name=_('lg column'))
    order_lg = models.PositiveIntegerField(default=1, verbose_name=_('lg order'))
    col_md = models.PositiveIntegerField(default=12, choices=COL_CHOICES, verbose_name=_('md column'))
    order_md = models.PositiveIntegerField(default=1, verbose_name=_('md order'))
    col_sm = models.PositiveIntegerField(default=12, choices=COL_CHOICES, verbose_name=_('sm column'))
    order_sm = models.PositiveIntegerField(default=1, verbose_name=_('sm order'))
    
    class Meta:
        abstract = True


class SectionModel(models.Model):
    """ Includes utility methods for content areas such as sections. """
    ALIGNMENT_CHOICES = (
        ('left', _('left')),
        ('centered', _('centered')),
        ('right', _('right')),
    )
    alignment = models.CharField(
        default='centered', 
        choices=ALIGNMENT_CHOICES, 
        max_length=50, 
        verbose_name=_('alignment')
    )
    POSITION_CHOICES = (
        (1, _('text first')),
        (3, _('text second')),
    )
    position = models.PositiveIntegerField(
        default=1, 
        choices=POSITION_CHOICES,
        verbose_name=_('text position')
    )

    class Meta:
        abstract = True

