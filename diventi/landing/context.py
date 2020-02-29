"""
    Custom context processors for the landing app.
    This script contains useful informations for landing templates.
"""
from .models import Section

def graph_section(request):
    """ Show featured sections to improve social networks sharing capabilities """
    graph_section = Section.objects.featured()
    context = {
        'graph_section': graph_section,
    }
    return context