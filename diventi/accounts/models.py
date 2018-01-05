from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from diventi.core.models import DiventiImageModel
from diventi.products.models import Product


class DiventiUserManager(auth_models.BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The email must be set'))
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
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(email, password, **extra_fields)


class DiventiAvatarQuerySet(models.QuerySet):

    # Fetch all users related to the avatar
    def users(self):
        avatar = self.diventiuser.all()
        return avatar


class DiventiAvatar(DiventiImageModel):    
    staff_only = models.BooleanField(default=False, verbose_name=_('staff_only'))

    objects = DiventiAvatarQuerySet.as_manager()

    class Meta:
        verbose_name = _('Avatar')
        verbose_name_plural = _('Avatars')


class DiventiCover(DiventiImageModel):

    objects = DiventiAvatarQuerySet.as_manager()

    class Meta:
        verbose_name = _('Cover')
        verbose_name_plural = _('Covers')

        
class DiventiUser(AbstractUser):    
    email = models.EmailField(unique=True, verbose_name=_('email'))
    avatar = models.ForeignKey(DiventiAvatar, blank=True, null=True, related_name='diventiuser', on_delete=models.SET_NULL, verbose_name=_('avatar'))
    cover = models.ForeignKey(DiventiCover, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('cover'))
    profilepic = models.ImageField(blank=True, upload_to='accounts/profilepics/', verbose_name=_('profilepic')) #  Staff use only
    bio = models.TextField(blank=True, verbose_name=_('bio'))
    role = models.CharField(blank=True, max_length=70, verbose_name=_('role')) # Favourite class

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = DiventiUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
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

