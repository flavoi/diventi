from django import forms

from captcha.fields import ReCaptchaField

from .models import DiventiUser


class DiventiUserCreationForm(forms.ModelForm):
    captcha = ReCaptchaField(
        attrs={
            'theme' : 'light',
        }
    )

    class Meta:
        model = DiventiUser
        fields = ('first_name', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'You Password'}),
        }


class DiventiUserUpdateForm(forms.ModelForm):
    path = '/static/image-picker/img/'
    AVATAR_CHOICES = ( 
        (path + 'page1.png', 'page1'), 
        (path + 'page2.png', 'page2'), 
        (path + 'page3.png', 'page3'), 
        (path + 'page4.png', 'page4'), 
    )
    profilepic = forms.ChoiceField(
        required=False, 
        choices=AVATAR_CHOICES,
        widget = forms.Select(attrs={'class': 'image-picker', 'name': 'profilepic'},),
    )

    class Meta:        
        model = DiventiUser
        fields = ['profilepic',]

