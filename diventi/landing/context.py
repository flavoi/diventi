"""
    Custom context processors for the landing app.
    This script contains useful informations for landing templates.
"""
from .models import (
	Section,
	SearchSuggestion,
    AboutArticle,
)

def graph_section(request):
    """ Show featured sections to improve social networks sharing capabilities """
    graph_section = Section.objects.featured()
    context = {
        'graph_section': graph_section,
    }
    return context

def search_suggestions(request):
	""" Returns the recommended search suggestions set by the authors. """
	search_suggestions = SearchSuggestion.objects.all()
	context = {
		'search_suggestions': search_suggestions,
	}
	return context

def about_us_articles(request):
    """ Returns the articles 'about us' listed in the footer. """
    about_us_articles = AboutArticle.objects.published()
    context = {
        'about_us_articles': about_us_articles,
    }
    return context