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

from diventi.core.models import (
    DiventiImageModel, 
    Element,
    TimeStampedModel,
)
from diventi.products.models import Product


class DiventiUserQuerySet(models.QuerySet):
    
    # Return active users
    def is_active(self):
        return self.filter(is_active=True)

    # Fetch all users that agreed to GDPR
    def has_agreed_gdpr(self):
        users = self.is_active()
        users = self.filter(has_agreed_gdpr=True)
        return users

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
        users = users.has_agreed_gdpr()
        users = users.filter(language=lan)
        return users

    # Returns the emails of users that set "lan" as main language
    def subscribers_emails(self, lan):
        users = self.subscribers(lan)
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

    def is_active(self):
        return self.get_queryset().is_active()

        
class DiventiAvatarQuerySet(models.QuerySet):

    # Fetch all users related to the avatar
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
        verbose_name = _('Deed')
        verbose_name_plural = _('Deeds')


class Role(Element):

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        

class DiventiUser(AbstractUser):
    nametag = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_('nametag')
    )
    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        verbose_name=_('language')
    )
    has_agreed_gdpr = models.NullBooleanField(
        verbose_name=_('subscriber status')
    )
    avatar = models.ForeignKey(
        DiventiAvatar,
        blank=True,
        null=True,
        related_name='diventiuser',
        on_delete=models.SET_NULL,
        verbose_name=_('avatar')
    )
    cover = models.ForeignKey(
        DiventiCover,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('cover')
    )
    profilepic = models.ForeignKey(
        DiventiProfilePic,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('profilepic')
    ) # For staff use only
    bio = models.TextField(
        blank=True,
        verbose_name=_('bio')
    )
    role = models.ForeignKey(
        Role,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('role')
    )
    deeds = models.ManyToManyField(
        Achievement,
        through = 'Award',
        verbose_name = _('deeds'),
        blank = True,
    )

    objects = DiventiUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('nametag', )
        permissions = (
            ("can_playtest", _("Can access playtest material")),
        )

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

    def get_diventi_role(self):
        if self.role:
            return self.get_diventi_username() + ' · {}'.format(self.role.title)
        else:
            return self.get_diventi_username()

    def search(self, query, *args, **kwargs):
        results = DiventiUser.objects.all().select_related('role')
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
                'title': user.get_diventi_role(),
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
        queryset = DiventiUser.objects.is_active()
        results = [] 
        last_subscriber = queryset.last_subscriber()
        prefix = _('Last subscriber')
        results.append({
            'columns': 6,
            'name': _("active users"),
            'title': queryset.count(),
            'description1': _('%(en)s english subscribers, %(it)s italian subscribers') % {
                'en': queryset.subscribers('en').count(),
                'it': queryset.subscribers('it').count(),
            },
            'description2': last_subscriber.get_description(prefix) if last_subscriber is not None else prefix + ': -',
            'action': '',
        })
        #results.append({
        #    'columns': 3,
        #    'name': _("english subscribers"),
        #    'title': queryset.subscribers_emails('en').count(),
        #    'action': {'label': _('copy emails'), 'function': 'copy-emails', 'parameters': queryset.subscribers_emails('en')},
        #})
        return results

    def __str__(self):
        return u'{0} ({1})'.format(self.get_short_name(), self.username)


class AwardQuerySet(models.QuerySet):

    # Prefetch all relevant data
    def related(self):
        awards = self.select_related('awarded_user')
        awards = awards.select_related('deed')
        return awards

    # Returns the users that were awarded with a certain achievement
    # with "lan" as main language
    def awarded_users(self, achievement, lan=None):
        awards = self.filter(achievement=achievement)
        awarded_users_id = awards.values_list('awarded_user')
        UserModel = get_user_model() 
        awarded_users = UserModel.objects.filter(id__in=awarded_users_id)
        if lan:
            awarded_users = awarded_users.filter(language=lan)
        awarded_users = awarded_users.is_active()
        return awarded_users

    # Returns the emails of users that were awarded with a certain achievement
    # with "lan" as main language
    def awarded_users_emails(self, achievement, lan):
        awarded_users = self.awarded_users(achievement, lan)
        awarded_users = awarded_users.has_agreed_gdpr()
        awarded_users = awarded_users.values_list('email', flat=True)
        return awarded_users

    # Returns the awards that have to be notified to the users
    def to_be_notified(self):
        awards = self.filter(notified=False)
        return awards
        

class Award(TimeStampedModel):

    deed = models.ForeignKey(
        Achievement, 
        on_delete = models.CASCADE, 
        verbose_name = _('deed')
    )
    awarded_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.CASCADE, 
        verbose_name = _('awarded user')
    )
    notified = models.BooleanField(
        default = False,
        verbose_name = _('notified')
    )

    objects = AwardQuerySet.as_manager()

    class Meta:
        verbose_name = _('Award')
        verbose_name_plural = _('Awards')


    def __str__(self):
        return _('Award: %(id)s') % {'id': self.id}

