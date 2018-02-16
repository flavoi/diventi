from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Feedback


class FeedbackCreationForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['description']        
        widgets = {            
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Tell us what you think!')}),            
        }