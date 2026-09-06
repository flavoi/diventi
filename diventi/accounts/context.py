from django.utils import translation
from django.utils.translation import get_language

def user_preferred_language(request):
    if request.user.is_authenticated:
        user_language = getattr(request.user, 'language', None)
        current_language = get_language()        
        if user_language and user_language != current_language:
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    # Evitiamo di restituire {'request': request} poiché Django lo inserisce già di default
    return {}
