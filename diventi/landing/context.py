"""
    Custom context processors for the landing app.
    This script contains useful informations for every template.
"""
from datetime import date

from .models import Presentation


def staff_special(request):
    """ Staff only buttons are rendered by this view. """
    p = Presentation.objects.active()
    staff_special = {
        'staff_special_url': p.staff_special_url,
        'staff_special_color': p.staff_special_color,
    }
    return staff_special