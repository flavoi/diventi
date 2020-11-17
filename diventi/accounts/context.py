"""
    Custom context processors for the accounts app.
    This script checks the user preferred language in every template.
"""

from django.utils import translation
from django.utils.translation import (
        get_language, 
        gettext_lazy as _,
)
from django.urls import reverse_lazy

from .utils import get_user_data


def user_preferred_language(request):
    if request.user.is_authenticated:
        user_language = request.user.language
        current_language = get_language()        
        if user_language != current_language:
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return {'request': request}


def user_statistics(request):
    context = {}
    if request.user.is_authenticated:
        context['authenticated_user_data'] = get_user_data(request.user)
    return context


class UserLink(object):
    label = ""
    icon = ""
    url = ""

    def __init__(self, label, icon, url):
        self.label = label
        self.icon = icon
        self.url = url

def user_menu(request):
    context = {}
    if request.user.is_authenticated:
        user_links = [
            UserLink(label=_('my profile'), icon='user', url=reverse_lazy('accounts:detail', args=(request.user.nametag,))),
            UserLink(label=_('settings'), icon='tools', url=reverse_lazy('accounts:settings', args=(request.user.nametag,))),
            UserLink(label=_('credentials'), icon='key', url=reverse_lazy('accounts:change_password', args=(request.user.nametag,))),
            UserLink(label=_('privacy'), icon='user-secret', url=reverse_lazy('accounts:change_privacy', args=(request.user.nametag,))),
        ]
        context = {
            'user_links': user_links, 
        }
    return context


