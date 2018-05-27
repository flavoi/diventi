"""
    Custom context processors for the landing app.
    This script contains a persistent feedback form in every template.
"""

from django.urls import reverse
from django.utils import translation

from .models import Feedback
from .forms import FeedbackCreationForm

def feedback_form(request):
    context = {
        'feedback_form': FeedbackCreationForm(),
        'feedback_count': Feedback.objects.usercount(),
    }
    return context