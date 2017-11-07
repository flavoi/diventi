from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse_lazy
from django.utils.html import mark_safe

from django.contrib.auth.models import BaseUserManager


class DiventiUserManager(auth_models.BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def members(self):
        return DiventiUser.objects.filter(is_staff=True).filter(member=True)


class DiventiAvatarQuerySet(models.QuerySet):

    # Fetch all users related to the avatar
    def users(self):
        avatar = self.diventiuser.all()
        return avatar 


class DiventiAvatar(models.Model):
    image = models.ImageField(blank=True, upload_to='accounts/avatars/')
    label = models.CharField(max_length=50, blank=True)
    staff_only = models.BooleanField()

    objects = DiventiAvatarQuerySet.as_manager()

    class Meta:
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatars'

    def image_tag(self):
        if self.image.url:
            return mark_safe('<img src="%s" height="42" width="42" />' % self.image.url)
        else:
            return u'(Nessuna immagine)'
    image_tag.short_description = 'Avatar'

    def __str__(self):
        return u'{0}'.format(self.label)

        
class DiventiUser(AbstractUser):    
    email = models.EmailField(unique=True)
    avatar = models.ForeignKey(DiventiAvatar, blank=True, null=True, related_name='diventiuser')
    profilepic = models.ImageField(blank=True, upload_to='accounts/profilepics/') # For the landing page, staff use only
    bio = models.TextField(blank=True)
    role = models.CharField(blank=True, max_length=70) # Favourite class
    member = models.BooleanField(default=False, help_text="If flagged the user will appear in the landing page") # If true the user appears in the landing page

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = DiventiUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id', )

    def get_absolute_url(self):
        return reverse_lazy('accounts:update', kwargs={'pk': self.pk})

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    def clean(self):
        # Set the first part of the email as username
        self.username = self.email

    def __str__(self):
        return u'{0} ({1})'.format(self.get_full_name(), self.email)

