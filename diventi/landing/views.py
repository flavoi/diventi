from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from .models import DiventiUser


def landing(request):
	""" 
		Renders the landing page with Diventi's main features and
		team members. 
	"""
	return render(request,
		"landing/landing.html",
		{
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
