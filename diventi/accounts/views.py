import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import AnonymousRequiredMixin

from diventi.core.views import DiventiActionMixin, StaffRequiredMixin
from diventi.products.models import Product
from diventi.comments.models import DiventiComment
from diventi.landing.models import Section

from .models import DiventiUser, DiventiAvatar, Achievement
from .forms import (
    DiventiAuthenticationForm,
    DiventiPasswordResetForm,
    DiventiUserCreationForm, 
    DiventiUserUpdateForm, 
    DiventiUserPrivacyChangeForm,
    DiventiSetPasswordForm,
    DiventiPasswordChangeForm,
)
from .utils import get_user_data


class DiventiLoginView(LoginView):

    authentication_form = DiventiAuthenticationForm
    form_class = DiventiAuthenticationForm
    template_name = "accounts/signin_quick.html"
    success_msg = _('You have signed in!')
    fail_msg = _('Your sign in has failed.')

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)        
        return super(DiventiLoginView, self).form_valid(form)


class DiventiLogoutView(LoginRequiredMixin, LogoutView):

	template_name = "accounts/signout_quick.html"


@login_required
@csrf_protect
def change_password_ajax(request):
    """
        Updates the user's password and returns the response as ajax.
    """
    message = ''
    error_message = ''
    if request.method == 'POST':
        form = DiventiPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            message = _('Your password was successfully updated!')
            message_type = 'success'
        else:  
            error_message = {str(form.fields[field].label): error for field, error in form.errors.items()}
            message_type = 'danger'
    data = json.dumps ({
        'message': str(message),
        'error_message': error_message,
        'message_type': message_type,
    })
    return HttpResponse(data, content_type='application/json')


@login_required
@csrf_protect
def change_privacy_ajax(request):
    """
        Updates user's privacy fields and returns the response as ajax.
    """
    message = ''
    error_message = ''
    if request.method == 'POST':
        form = DiventiUserPrivacyChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            message = _('Your privacy was successfully updated!')
            message_type = 'success'
        else:
            error_message = {str(form.fields[field].label): error for field, error in form.errors.items()}
            message_type = 'danger'
    data = json.dumps ({
        'message': str(message),
        'error_message': error_message,
        'message_type': message_type,
    })
    return HttpResponse(data, content_type='application/json')    


class DiventiUserCreationView(AnonymousRequiredMixin, CreateView):

    form_class = DiventiUserCreationForm
    model = DiventiUser
    template_name = 'accounts/signup_quick.html'
    success_msg = _('You have signed up!')
    fail_msg = _('Your sign up has failed.')
    fail_url = reverse_lazy('accounts:signup')

    def get_initial(self):
        # Retrieve initial data from user inputs on the landing page
        initial_email = self.request.session.get('initial_email', None)
        initial_first_name = self.request.session.get('initial_first_name', None)
        initial = {
            'email': initial_email,
            'first_name': initial_first_name,
        }
        return initial

    def get_success_url(self):
        self.request.session['show_login_form'] = 1
        return reverse_lazy('landing:home')

    def form_valid(self, form, inital_group='Community'):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        if email and password:
            form.save()
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                user_group, created = Group.objects.get_or_create(name=inital_group)
                user.groups.add(user_group)
                user.save()
                messages.success(self.request, self.success_msg)
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                messages.error(self.request, self.fail_msg)
        return super().form_valid(form)


class DiventiUserUpdateView(LoginRequiredMixin, DiventiActionMixin, UpdateView):

    form_class = DiventiUserUpdateForm
    model = DiventiUser
    template_name = "accounts/user_settings_quick.html"
    success_msg = _('Profile updated!')
    fail_msg = _('Profile has not been updated.')
    slug_field = 'nametag'
    slug_url_kwarg = 'nametag'

    def user_passes_test(self):
        """ A user may update his own profile only. """
        if self.object.pk == self.request.user.pk:
            return 1
        return 0

    def get_success_url(self):        
        return reverse('accounts:settings', kwargs={'nametag': self.object.nametag})

    def get_form_kwargs(self):
        """ Inject form with additional keyword arguments. """
        kwargs = super(DiventiUserUpdateView, self).get_form_kwargs()
        if not self.user_passes_test():
            raise PermissionDenied(_("A user may update his own profile only."))
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DiventiUserUpdateView, self).get_context_data(**kwargs)        
        context = get_user_data(context, self.request.user)
        privacy_form = DiventiUserPrivacyChangeForm(instance=self.request.user)
        context['privacy_form'] = privacy_form
        return context


class DiventiUserPasswordChangeView(LoginRequiredMixin, DiventiActionMixin, PasswordChangeView):

    model = DiventiUser
    form_class = DiventiPasswordChangeForm
    template_name = "accounts/user_change_password_quick.html"


class DiventiUserPrivacyChangeView(LoginRequiredMixin, DiventiActionMixin, UpdateView):

    model = DiventiUser
    form_class = DiventiUserPrivacyChangeForm
    template_name = "accounts/user_change_privacy_quick.html"
    slug_field = 'nametag'
    slug_url_kwarg = 'nametag'


class DiventiUserDetailView(DetailView):

    model = DiventiUser
    template_name = "accounts/user_detail_quick.html"
    slug_field = 'nametag'
    slug_url_kwarg = 'nametag'

    def get_context_data(self, **kwargs):
        context = super(DiventiUserDetailView, self).get_context_data(**kwargs)
        context = get_user_data(context, self.object, self.request.user)
        return context


class DiventiUserDeleteView(LoginRequiredMixin, DiventiActionMixin, DeleteView):

    model = DiventiUser
    slug_field = 'nametag'
    slug_url_kwarg = 'nametag'
    success_url = reverse_lazy('landing:home')
    success_msg = _('Your profile has been deleted.')

    def post(self, *args, **kwargs):
        """ Delete user related objects upon user deletion. """
        comments = DiventiComment.objects.filter(user=self.request.user)
        if comments:
            comments.update(is_removed=True)
        return super(DiventiUserDeleteView, self).post(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return super(DiventiUserDeleteView, self).get_success_url()


class EmailPageView(StaffRequiredMixin, TemplateView):

    template_name = "accounts/subscribers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = DiventiUser.objects.all()
        users_count = users.count()                
        users_groups = users.emails()
        subscribers = users.has_agreed_gdpr()
        subscribers_groups = subscribers.emails()
        users_lan = {}
        for ugroup in users_groups:
            lan = ugroup['language']
            users_lan[lan] = users.filter(language=lan)
        subscribers_lan = {}
        for sgroup in subscribers_groups:
            lan = sgroup['language']
            subscribers_lan[lan] = subscribers.filter(language=lan)
        context['users_count'] = users_count
        context['users_groups'] = users_groups
        context['users_lan'] = users_lan
        context['subscribers_groups'] = subscribers_groups
        context['subscribers_lan'] = subscribers_lan
        context['msg_success'] = _('The email addresses have been copied to clipboard.')
        context['msg_failure'] = _('Something went wrong with the copy.')
        return context


class DiventiPasswordResetView(PasswordResetView):
    
    form_class = DiventiPasswordResetForm
    template_name = 'accounts/password_reset_form_quick.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class DiventiPasswordResetDoneView(PasswordResetDoneView):

    template_name = 'accounts/password_reset_done_quick.html'


class DiventiPasswordResetConfirmView(PasswordResetConfirmView):

    form_class = DiventiSetPasswordForm
    template_name='accounts/password_reset_confirm_quick.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class DiventiPasswordResetCompleteView(PasswordResetCompleteView):

    template_name='accounts/password_reset_complete_quick.html'

    