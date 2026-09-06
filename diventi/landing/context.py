from django.core.cache import cache
from .models import LandingPage, SearchSuggestion, AboutArticle

def graph_section(request):
    try:
        page = LandingPage.objects.featured()
        graph_sec = page.sections.featured()
    except Exception:
        graph_sec = None
    return {'graph_section': graph_sec}


def search_suggestions(request):
    suggestions = cache.get('global_search_suggestions')
    if suggestions is None:
        suggestions = list(SearchSuggestion.objects.all())
        cache.set('global_search_suggestions', suggestions, 3600)
    return {'search_suggestions': suggestions}


def about_us_articles(request):
    about_articles = cache.get('global_about_us_articles')
    if about_articles is None:
        about_articles = list(AboutArticle.objects.published())
        cache.set('global_about_us_articles', about_articles, 3600)
    return {'about_us_articles': about_articles}