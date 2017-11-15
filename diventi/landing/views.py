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
    return render(request,
        "landing/landing.html",
        {    
            "presentation": presentation,
            "staff": staff,
        },
    )
