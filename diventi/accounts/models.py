from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import models as auth_models


class DiventiUserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = user.is_staff = True
        user.save(using=self._db)
        return user


class DiventiUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True, upload_to='avatars/')
    bio = models.TextField(blank=True)
    role = models.CharField(blank=True, max_length=70)

    objects = DiventiUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id', )

    def __unicode__(self):
        return u'{0} ({1})'.format(self.get_full_name(), self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)