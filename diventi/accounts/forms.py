from django import forms

from captcha.fields import ReCaptchaField

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

    class Meta:        
        model = DiventiUser
        fields = ['avatar', 'bio', 'role']
        labels = {
            'role': 'Favourite class',
        }
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control',}),
            'role': forms.TextInput(attrs={'class': 'form-control',}),
        }

    def get_avatar_queryset(self):
        """ Fetch special avatars if the user is an admin."""
        user = self.user
        avatar_queryset = DiventiAvatar.objects.all().order_by('-staff_only')
        if user and not user.is_staff:
            avatar_queryset = avatar_queryset.filter(staff_only=False)
        print(avatar_queryset)        
        return avatar_queryset                    

    avatar = forms.ModelChoiceField(
        queryset = DiventiAvatar.objects.all(),
        widget = DiventiAvatarSelect(),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')        
        super(DiventiUserUpdateForm, self).__init__(*args, **kwargs)        
        self.fields['avatar'].queryset = self.get_avatar_queryset()
