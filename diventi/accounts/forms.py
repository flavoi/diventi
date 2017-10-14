from django import forms

from captcha.fields import ReCaptchaField

from .models import DiventiUser


class DiventiUserCreationForm(forms.ModelForm):
    captcha = ReCaptchaField(attrs={
      'theme' : 'light',      
    })

    class Meta:
        model = DiventiUser
        fields = ('first_name', 'email', 'password', 'captcha')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'You Password'}),
        }