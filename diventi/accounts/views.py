import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from braces.views import AnonymousRequiredMixin, LoginRequiredMixin

from .models import DiventiUser, DiventiAvatar, Achievement
from .forms import DiventiUserCreationForm, DiventiUserUpdateForm
from .utils import get_user_data
from diventi.core.views import DiventiActionMixin
from diventi.products.models import Product


class DiventiLoginView(AnonymousRequiredMixin, LoginView):

    template_name = "accounts/signin.html"
    success_msg = _('You have signed in!')
    fail_msg = _('Your sign in has failed.')
    fail_url = reverse_lazy('landing:home')

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:            
            return next_url
        else:
            super().get_success_url()

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)        
        return super(DiventiLoginView, self).form_valid(form)
    
    def form_invalid(self, form):
        # This session variable must be managed by the fail_url view
        self.request.session['show_login_form'] = 1
        self.request.session['fail_login_msg'] = str(self.fail_msg)        
        return redirect(self.fail_url)
        

class DiventiLogoutView(LoginRequiredMixin, LogoutView):

	template_name = "accounts/signout.html"


@login_required
@csrf_protect
def change_password_ajax(request):
    message = ''
    error_message = ''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
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


class DiventiUserCreationView(AnonymousRequiredMixin, CreateView):

    form_class = DiventiUserCreationForm
    model = DiventiUser
    template_name = 'accounts/signup.html'
    success_msg = _('You have signed up!')
    fail_msg = _('Your sign up has failed.')
    success_url = reverse_lazy('landing:home')

    def get_initial(self):
        # Retrieve initial data from user inputs on the landing page
        initial_username = self.request.session.get('initial_username', None)
        initial_first_name = self.request.session.get('initial_first_name', None)
        initial = {
            'username': initial_username,
            'first_name': initial_first_name,
        }
        return initial

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        if username and password:
            form.save()
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                messages.success(self.request, self.success_msg)
                self.request.session['show_login_form'] = 1
                return redirect(self.success_url)
            else:
                messages.error(self.request, self.fail_msg)
        return super(DiventiUserCreationView, self).form_valid(form)


    def form_invalid(self, form):
        print(form.errors)
        return super(DiventiUserCreationView, self).form_invalid(form)


class DiventiUserUpdateView(LoginRequiredMixin, DiventiActionMixin, UpdateView):

    form_class = DiventiUserUpdateForm
    model = DiventiUser
    template_name = "accounts/user.html"
    success_msg = _('Profile updated!')
    fail_msg = _('Profile has not been updated.')

    def user_passes_test(self):
        """ A user may update his own profile only. """
        if self.object.pk == self.request.user.pk:
            return 1
        return 0

    def get_form_kwargs(self):
        """ Inject form with additional keyword arguments. """
        kwargs = super(DiventiUserUpdateView, self).get_form_kwargs()
        if not self.user_passes_test():
            raise PermissionDenied(_("A user may update his own profile only."))
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DiventiUserUpdateView, self).get_context_data(**kwargs)        
        context = get_user_data(context, self.request.user)
        return context


class DiventiUserDetailView(DetailView):

    model = DiventiUser
    template_name = "accounts/detail.html"

    def get_context_data(self, **kwargs):
        context = super(DiventiUserDetailView, self).get_context_data(**kwargs)
        context = get_user_data(context, self.object, self.request.user)
        return context


class DiventiUserDeleteView(LoginRequiredMixin, DiventiActionMixin, DeleteView):

    model = DiventiUser
    success_url = reverse_lazy('landing:home')
    success_msg = _('Your profile has been deleted.')
