from functools import reduce
import operator

from django.db import models
from django.db.models import Q, Count, Sum
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify
from django.contrib.humanize.templatetags.humanize import naturalday

from diventi.core.models import DiventiImageModel, Element
from diventi.products.models import Product


class DiventiUserQuerySet(models.QuerySet):
    
    # Return active users
    def is_active(self):
        return self.filter(is_active=True)

    # Fetch all users that agreed to GDPR
    def has_agreed_gdpr(self):
        users = self.is_active()
        users = self.filter(has_agreed_gdpr=True)
        return users

    # Fetch all the achievements related to the user
    def achievements(self):
        user = self.prefetch_related('achievements')
        return user

    # Fetch all users that made at least a product
    def authors(self):
        products = Product.objects.all()
        users = self.filter(products__in=products)
        return users

    # Returns the emails of a group of users
    def emails(self):
        return self.values('language').annotate(total=Count('email')).order_by('language')

    # Returns the users that set "lan" as main language
    def subscribers(self, lan):
        users = self.is_active()
        users = self.filter(language=lan)
        return users

    # Returns the emails of users that set "lan" as main language
    def subscribers_emails(self, lan):
        users = self.subscribers(lan)
        users = users.has_agreed_gdpr()
        emails = users.values_list('email', flat=True)
        return emails

    # Returns the last user that has signed up and agreed to gdpr
    # with "lan" as main language 
    def last_subscriber(self, lan=None):
        users = self.is_active()
        if lan:
            users = users.filter(language=lan)
        user = users.order_by('-date_joined').first()
        return user


class DiventiUserManager(UserManager):

    def get_queryset(self):
        return DiventiUserQuerySet(self.model, using=self._db)

    def has_agreed_gdpr(self):
        return self.get_queryset().has_agreed_gdpr()

    def achievements(self):
        return self.get_queryset().achievements()

    def authors(self):
        return self.get_queryset().authors()

    def emails(self):
        return self.get_queryset().emails()

    def subscribers(self, lan):
        return self.get_queryset().subscribers(lan)

    def subscribers_emails(self, lan):
        return self.get_queryset().lan_emails(lan)

    def last_subscriber(self, lan):
        return self.get_queryset().last_subscriber(lan)

        
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


class DiventiProfilePic(DiventiImageModel):    
    
    class Meta:
        verbose_name = _('Profile picture')
        verbose_name_plural = _('Profile pictures')


class DiventiCover(DiventiImageModel):

    objects = DiventiAvatarQuerySet.as_manager()

    class Meta:
        verbose_name = _('Cover')
        verbose_name_plural = _('Covers')


class Achievement(Element):

    class Meta:
        verbose_name = _('Achievement')
        verbose_name_plural = _('Achievements')


class Role(Element):

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        

class DiventiUser(AbstractUser):
    nametag = models.SlugField(max_length=200, unique=True, verbose_name=_('nametag'))
    language = models.CharField(blank=True,  max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_('language'))
    has_agreed_gdpr = models.NullBooleanField(blank=True, verbose_name=_('subscriber status'))
    avatar = models.ForeignKey(DiventiAvatar, blank=True, null=True, related_name='diventiuser', on_delete=models.SET_NULL, verbose_name=_('avatar'))
    cover = models.ForeignKey(DiventiCover, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('cover'))
    profilepic = models.ForeignKey(DiventiProfilePic, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('profilepic')) # For staff use only
    bio = models.TextField(blank=True, verbose_name=_('bio'))
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('role'))
    achievements = models.ManyToManyField(Achievement, related_name='users')

    objects = DiventiUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('nametag', )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.nametag = '-'.join((slugify(self.get_short_name()), slugify(self.pk)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('accounts:detail', kwargs={'nametag': self.nametag})

    def class_name(self):
        return _('account')

    def clean(self):
        # Set the email as username
        self.username = self.email

    def get_diventi_username(self):
        if self.first_name: 
            return self.get_full_name()
        else:
            return self.get_username()

    def search(self, query, *args, **kwargs):
        results = DiventiUser.objects.all()
        query_list = query.split()
        queryset = results.filter(
            reduce(operator.and_,
                   (Q(first_name__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(role__title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(bio__icontains=q) for q in query_list))
        )
        results = []
        for user in queryset:
            row = {
                'class_name': user.class_name(),
                'title': user.first_name,
                'description': user.bio,
                'get_absolute_url': user.get_absolute_url()
            }
            results.append(row)
        return results

    # Returns the description of the subscriber
    # Or none if none is found
    def get_description(self, prefix):
        description = _('%(prefix)s: %(last_sub)s on %(date_joined)s') % {
            'prefix': prefix,
            'last_sub': self.get_short_name(),
            'date_joined': naturalday(self.date_joined),
        }
        return description

    def reporting(self, *args, **kwargs):    
        queryset = DiventiUser.objects.all().is_active()
        results = [] 
        last_subscriber = queryset.last_subscriber()
        prefix = _('Last subscriber')
        results.append({
            'columns': 6,
            'name': _("users count"),
            'title': queryset.count(),
            'description1': _('%(en)s english subscribers, %(it)s italian subscribers') % {
                'en': queryset.subscribers('en').count(),
                'it': queryset.subscribers('it').count(),
            },
            'description2': last_subscriber.get_description(prefix) if last_subscriber is not None else prefix + ': -',
            'action': '',
        })
        results.append({
            'columns': 3,
            'name': _("english subscribers"),
            'title': queryset.subscribers_emails('en').count(),
            'action': {'label': _('copy emails'), 'function': 'copy-emails', 'parameters': queryset.subscribers_emails('en')},
        })
        results.append({
            'columns': 3,
            'name': _("italian subscribers"),
            'title': queryset.subscribers_emails('it').count(),
            'action': {'label': _('copy emails'), 'function': 'copy-emails', 'parameters': queryset.subscribers_emails('it')},
        })
        return results

    def __str__(self):
        return u'{0} ({1})'.format(self.get_short_name(), self.username)
