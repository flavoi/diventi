from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


class DiventiLoginView(LoginView):
	"""
		Logic dedicated to user sign-in.
	"""
	template_name = "accounts/login.html"


class DiventiLogoutView(LogoutView):
	"""
		Logic dedicated to user sign-out.
	"""
	template_name = "accounts/logout.html"
