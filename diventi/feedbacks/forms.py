from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('survey', 'question', 'content')        
        widgets = {
            'survey': forms.HiddenInput,
            'question': forms.HiddenInput,
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }