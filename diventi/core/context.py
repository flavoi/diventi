"""
    Custom context processors for the core app.
    This script contains useful informations for every template.
"""
from datetime import date

def footer(request):
    """ Automatic signature: Diventi YYYY-YYYY """
    START_YEAR = 2017
    this_year = date.today().year
    if START_YEAR != this_year:
        copy_year = "%s - %s" % (START_YEAR, this_year)
    else:
        copy_year = START_YEAR
    signature = {
        'copy': "%s" % copy_year,
    }
    return signature