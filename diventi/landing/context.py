"""
    Custom context processors for the core landing.
    This script contains a persistent feedback form in every template.
"""

from django.core.urlresolvers import reverse

from .models import Feedback
from .forms import FeedbackCreationForm

def feedback_form(request):

    context = {
        'feedback_form': FeedbackCreationForm(),
        'feedback_count': Feedback.objects.usercount(),
    }
    return context