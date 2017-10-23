from django import forms

from captcha.fields import ReCaptchaField
from cuser.middleware import CuserMiddleware

from .models import DiventiUser, DiventiAvatar
from .widgets import DiventiAvatarSelect

class DiventiUserCreationForm(forms.ModelForm):
    captcha = ReCaptchaField(
        attrs={
            'theme' : 'light',
        }
    )

    class Meta:
        model = DiventiUser
        fields = ['first_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'You Password'}),
        }


class DiventiUserUpdateForm(forms.ModelForm):

    avatar = forms.ModelChoiceField(
        queryset = DiventiAvatar.objects.all(),
        widget = DiventiAvatarSelect(),
    )

    def __init__(self, *args, **kwargs):
        super(DiventiUserUpdateForm, self).__init__(*args, **kwargs)        
        
    class Meta:        
        model = DiventiUser
        fields = ['avatar', 'bio', 'role']
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control',}),
            'role': forms.TextInput(attrs={'class': 'form-control',}),
        }