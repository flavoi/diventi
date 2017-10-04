from django import forms

from .models import DiventiUser


class DiventiUserCreationForm(forms.ModelForm):

    class Meta:
        model = DiventiUser
        fields = ('first_name', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'You Password'}),
        }