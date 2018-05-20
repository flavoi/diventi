from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField

from .models import DiventiUser, DiventiAvatar, DiventiCover
from .widgets import DiventiAvatarSelect, DiventiCoverSelect, DiventiAvatarChoiceField, DiventiCoverChoiceField


class DiventiUserCreationForm(UserCreationForm):
    
    captcha = ReCaptchaField(
        attrs={
            'theme' : 'light',
        }
    )

    class Meta:
        model = DiventiUser
        fields = ['first_name', 'email', 'password1', 'password2', 'language']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your email')}),
            'language': forms.Select(attrs={'class': 'form-control',})         
        }

    def __init__(self, *args, **kwargs):
        super(DiventiUserCreationForm, self).__init__(*args, **kwargs)
        """ Somehow the widgets for the password fields must be managed in the constructor. """
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Your password')
            })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Repeat your password'),
            })


class DiventiUserInitForm(forms.ModelForm):

    class Meta:
        model = DiventiUser
        fields = ['first_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your email')}),            
        }


class DiventiUserUpdateForm(forms.ModelForm):  

    class Meta:        
        model = DiventiUser
        fields = ['avatar', 'cover', 'bio', 'role', 'language']
        labels = {
            'bio': _("What's your story?"),
            'role': _("What's your favourite class?"),
        }
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control',}),
            'role': forms.TextInput(attrs={'class': 'form-control',}),
            'language': forms.Select(attrs={'class': 'form-control',})
        }

    def get_avatar_queryset(self):
        """ Fetch special avatars if the user is an admin."""
        user = self.user
        avatar_queryset = DiventiAvatar.objects.all().order_by('-staff_only')
        if user and not user.is_staff:
            avatar_queryset = avatar_queryset.filter(staff_only=False)        
        return avatar_queryset

    avatar = DiventiAvatarChoiceField(
        queryset = DiventiAvatar.objects.none(),
        widget = DiventiAvatarSelect(attrs = {
            'class': 'image-picker show-html'
        }),
        required = False,
    )

    cover = DiventiCoverChoiceField(
        queryset = DiventiCover.objects.none(),
        widget = DiventiCoverSelect(attrs = {
            'class': 'image-picker show-html'
        }),
        required = False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')        
        super(DiventiUserUpdateForm, self).__init__(*args, **kwargs)        
        self.fields['avatar'].queryset = self.get_avatar_queryset()
        self.fields['cover'].queryset = DiventiCover.objects.all()    
