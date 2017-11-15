from django.shortcuts import render

from .models import Presentation
from diventi.accounts.models import DiventiUser


def landing(request):
    """ 
        Renders the landing page with Diventi's main features and
        team members. 
    """
    presentation = Presentation.objects.active()
    staff = DiventiUser.objects.members()
    NCOLUMNS = 3
    i = 0
    events = presentation.events.all().order_by('event_date')
    events_columns = []
    for k in range(0, NCOLUMNS):
        events_columns.append([])
    for ev in events:
        events_columns[i].append(ev)
        if i < NCOLUMNS - 1:
            i += 1
        elif i == NCOLUMNS - 1:
            i = 0
    return render(request,
        "landing/landing.html",
        {    
            "presentation": presentation,
            "staff": staff,
            "events_columns": events_columns,
        },
    )
