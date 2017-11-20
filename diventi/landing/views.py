from django.shortcuts import render, redirect

from .models import Presentation
from diventi.accounts.models import DiventiUser
from diventi.accounts.forms import DiventiUserInitForm
from diventi.products.models import Product


def landing(request):
    """ 
        Renders the landing page with Diventi's main features and
        team members. 
    """
    presentation = Presentation.objects.active()
    staff = DiventiUser.objects.members()
    featured_product = Product.objects.featured()
    if request.method == 'POST':
        registration_form = DiventiUserInitForm(request.POST)
        if registration_form.is_valid():
            # Save the user inputs and pass them to the sign up page
            request.session['initial_email'] = registration_form['email'].value()
            request.session['initial_first_name'] = registration_form['first_name'].value()
            return redirect('accounts:signup')
    else:
        registration_form = DiventiUserInitForm()
    return render(request,
        'landing/landing.html',
        {    
            'presentation': presentation,
            'staff': staff,
            'registration_form': registration_form,
            'featured_product': featured_product,
        },
    )
