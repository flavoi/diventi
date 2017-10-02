from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput

from .models import DiventiUser


class DiventiUserCreationForm(UserCreationForm):

    class Meta:
        model = DiventiUser
        fields = ("email", "avatar", "password1", "password2")
        widgets = {
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...'}),            
            'password1': PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password..."}),
            'password2': PasswordInput(attrs={'class': 'form-control', 'placeholder': "Repeat the password..."}),
        }