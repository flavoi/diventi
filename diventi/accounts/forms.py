from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm, 
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
)
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives

from captcha.fields import ReCaptchaField
from cuser.middleware import CuserMiddleware


from diventi.core.utils import send_diventi_email

from .models import (
    DiventiUser,
    DiventiAvatar,
    DiventiCover,
    Role,
)
from .widgets import (
    DiventiAvatarSelect, 
    DiventiCoverSelect, 
    DiventiAvatarChoiceField, 
    DiventiCoverChoiceField,
)


BOOL_CHOICES = ((True, _("Yes, I'm interested.")), (False, _("No, don't send me emails.")))


class DiventiPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(DiventiPasswordChangeForm, self).__init__(*args, **kwargs)
        """ Somehow the widgets for the password fields must be managed in the constructor. """
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            })
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            })


class DiventiSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(DiventiSetPasswordForm, self).__init__(*args, **kwargs)
        """ Somehow the widgets for the password fields must be managed in the constructor. """
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-prepend', 
            'placeholder': '********'
            })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-prepend',
            'placeholder': '********'
            }) 


class DiventiPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        required=True,
        label = _('Email address'),
        widget = forms.EmailInput(attrs={
            'class': 'form-control form-control-prepend',
            'placeholder': _('name@example.com'),
        })
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        html_email = ''
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        send_diventi_email(
            subject = subject,
            message = body,
            from_email = 'autori@playdiventi.it',
            recipient_list = [to_email],
            from_name = 'Diventi',
            html_message = None,
        )


class DiventiAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(DiventiAuthenticationForm, self).__init__(*args, **kwargs)
        """ Somehow the widgets must be managed in the constructor. """
        self.fields['username'].widget = forms.EmailInput(attrs={
                 'class': 'form-control form-control-prepend',
                 'placeholder': _('name@example.com'),
             })
        self.fields['password'].widget = forms.PasswordInput(attrs={
             'class': 'form-control form-control-prepend',
             'placeholder': '********'
             })    


class DiventiUserCreationForm(UserCreationForm):

    captcha = ReCaptchaField(
        attrs={
            'theme' : 'light',
        }
    )

    class Meta:
        model = DiventiUser
        fields = ['first_name', 'email', 'password1', 'password2', 'language', 'has_agreed_gdpr']
        labels = {
            'has_agreed_gdpr': _('Can we send you emails?'), 
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-prepend', 
                'placeholder': _('Mario Rossi'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-prepend',
                 'placeholder': _('name@example.com'),
                 'required': True,
            }),
            'language': forms.Select(attrs={
                'class': 'custom-select',
            }),
            'has_agreed_gdpr': forms.RadioSelect(
                choices=BOOL_CHOICES,
                attrs={
                    'class': 'custom-control-input',
                    'required': True,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(DiventiUserCreationForm, self).__init__(*args, **kwargs)
        """ Somehow the widgets for the password fields must be managed in the constructor. """
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-prepend', 
            'placeholder': '********'
            })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-prepend',
            'placeholder': '********'
            })

    def clean_email(self):
        email = self.cleaned_data['email']
        email_has_been_used = DiventiUser.objects.filter(email=email).exists()
        if email_has_been_used:
            raise forms.ValidationError( _('This email has already been used.'))
        if email is None or email == '':
            raise forms.ValidationError( _('Please, fill in your email to complete the registration.'))            
        return email

    def clean_has_agreed_gdpr(self):
        has_agreed_gdpr = self.cleaned_data['has_agreed_gdpr']
        if has_agreed_gdpr is None:
            raise forms.ValidationError( _('Please, let us know if we can send emails to you.'))
        return has_agreed_gdpr


class DiventiUserInitForm(forms.Form):
    first_name = forms.CharField(
        max_length = 30, 
        widget = forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': _('Your name')
        }),
    )
    email = forms.EmailField(
        max_length=30, 
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your email')
        })
    )


class DiventiUserUpdateForm(forms.ModelForm):

    class Meta:       
        model = DiventiUser
        fields = ['first_name', 'avatar', 'cover', 'bio', 'role', 'language']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 1,
                'data-toggle': 'autosize',
            }),
            'role': forms.Select(attrs={
                'class': 'custom-select',
            }),
            'language': forms.Select(attrs={
                'class': 'custom-select',
            }),
        }

    avatar = DiventiAvatarChoiceField(
        queryset = DiventiAvatar.objects.all(),
        widget = DiventiAvatarSelect(attrs = {
            'class': 'image-picker show-labels show-html'
        }),
        required = False,
    )

    cover = DiventiCoverChoiceField(
        queryset = DiventiCover.objects.all(),
        widget = DiventiCoverSelect(attrs = {
            'class': 'image-picker show-labels show-html'
        }),
        required = False,
    )

    def get_avatar_queryset(self):
        """ Fetch special avatars if the user is an admin."""
        user = CuserMiddleware.get_user()
        avatar_queryset = DiventiAvatar.objects.all().order_by('-staff_only')
        if not user or not user.is_staff:
            avatar_queryset = avatar_queryset.filter(staff_only=False)  
        return avatar_queryset

    def __init__(self, *args, **kwargs):
        super(DiventiUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].queryset = self.get_avatar_queryset()


class DiventiUserPrivacyChangeForm(forms.ModelForm):

    class Meta:       
        model = DiventiUser
        fields = ['has_agreed_gdpr']
        labels = {
            'has_agreed_gdpr': _("Can we send you emails?"),
        }
        widgets = {
            'has_agreed_gdpr': forms.RadioSelect(
                choices=BOOL_CHOICES, 
                attrs={
                    'class': 'custom-control-input',
                }),
        }

