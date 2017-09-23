from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from .models import DiventiUser, Profile


def landing(request):
	""" 
		Renders the landing page with Diventi's main features and
		team members. 
	"""
	try:
		active_profile = Profile.objects.get(active=True)
	except Profile.DoesNotExist:
		msg = "There is no active profile."
		raise Profile.DoesNotExist(msg)
	except Profile.MultipleObjectsReturned:
		msg = "There must be only one profile at a time. Please fix!"
		raise Profile.MultipleObjectsReturned(msg)
		
	return render(request,
		"landing/landing.html",
		{	
			"profile": active_profile,
			"staff": DiventiUser.objects.filter(is_staff=True),
		},
	)


class DiventiLoginView(LoginView):
	"""
		Logic dedicated to user sign-in.
	"""
	template_name = "landing/login.html"


class DiventiLogoutView(LogoutView):
	"""
		Logic dedicated to user sign-out.
	"""
	template_name = "landing/logout.html"
