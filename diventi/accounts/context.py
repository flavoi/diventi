"""
    Custom context processors for the accounts app.
    This script checks the user preferred language in every template.
"""

from django.utils import translation


def user_preferred_language(request):
    if request.user.is_authenticated():        
        user_language = request.user.language
        if user_language:
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return request
