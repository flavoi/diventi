from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from captcha.fields import ReCaptchaField
from cuser.middleware import CuserMiddleware

from .models import DiventiUser, DiventiAvatar, DiventiCover
from .widgets import DiventiAvatarSelect, DiventiCoverSelect, DiventiAvatarChoiceField, DiventiCoverChoiceField


BOOL_CHOICES = ((True, _("Yes, I'm interested.")), (False, _("No, don't send me emails.")))


class DiventiUserCreationForm(UserCreationForm):
    
    captcha = ReCaptchaField(
        attrs={
            'theme' : 'light',
        }
    )

    class Meta:
        model = DiventiUser
        fields = ['first_name', 'username', 'password1', 'password2', 'language', 'has_agreed_gdpr']
        labels = {
            'has_agreed_gdpr': _('Can we send you emails?'), 
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your name')}),
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your email')}),
            'language': forms.Select(attrs={'class': 'form-control',}),
            'has_agreed_gdpr': forms.RadioSelect(choices=BOOL_CHOICES, attrs={'class': 'form-check-input',}),
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


class DiventiUserInitForm(forms.Form):
    first_name = forms.CharField(
        max_length = 30, 
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your name')}),
    )
    username = forms.EmailField(
        max_length=30, 
        widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your email')})
    )


class DiventiUserUpdateForm(forms.ModelForm):     

    class Meta:       
        model = DiventiUser
        fields = ['avatar', 'cover', 'bio', 'role', 'language', 'has_agreed_gdpr']
        labels = {
            'bio': _("What's your story?"),
            'role': _("What's your favourite class?"),
            'has_agreed_gdpr': _("Can we send you emails?"),
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows':4,}),
            'role': forms.TextInput(attrs={'class': 'form-control',}),
            'language': forms.Select(attrs={'class': 'form-control',}),
            'has_agreed_gdpr': forms.RadioSelect(choices=BOOL_CHOICES, attrs={'class': 'form-check-input',}),
        }

    def get_avatar_queryset():
        """ Fetch special avatars if the user is an admin."""
        user = CuserMiddleware.get_user()
        avatar_queryset = DiventiAvatar.objects.all().order_by('-staff_only')
        if user and not user.is_staff:
            avatar_queryset = avatar_queryset.filter(staff_only=False)        
        return avatar_queryset

    avatar = DiventiAvatarChoiceField(
        queryset = get_avatar_queryset(),
        widget = DiventiAvatarSelect(attrs = {
            'class': 'image-picker show-html'
        }),
        required = False,
    )

    cover = DiventiCoverChoiceField(
        queryset = DiventiCover.objects.all(),
        widget = DiventiCoverSelect(attrs = {
            'class': 'image-picker show-html'
        }),
        required = False,
    )
