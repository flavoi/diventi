from django.shortcuts import render
from django.views.generic import TemplateView

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
