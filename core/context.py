"""
    Custom context processors for the page app.
    This script contains useful informations for every template.
"""
from datetime import date

from django.conf import settings
from django.shortcuts import get_object_or_404


def signature(request):
    """ Automatic signature: Diventi YYYY-YYYY """
    START_YEAR = 2017
    this_year = date.today().year
    if START_YEAR != this_year:
        copy_year = "%s - %s" % (START_YEAR, this_year)
    else:
        copy_year = START_YEAR
    signature = {
        'copy': "Diventi %s" % copy_year,
    }
    return signature