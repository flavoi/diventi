from django.shortcuts import render, redirect

from .models import Presentation
from diventi.accounts.models import DiventiUser
from diventi.accounts.forms import DiventiUserInitForm


def landing(request):
    """ 
        Renders the landing page with Diventi's main features and
        team members. 
    """
    presentation = Presentation.objects.active()
    staff = DiventiUser.objects.members()
    if request.method == "POST":
        registration_form = DiventiUserInitForm(request.POST)
        if registration_form.is_valid():
            return redirect('accounts:signup')
    else:
        registration_form = DiventiUserInitForm()
    return render(request,
        "landing/landing.html",
        {    
            "presentation": presentation,
            "staff": staff,
            "registration_form": registration_form,
        },
    )
