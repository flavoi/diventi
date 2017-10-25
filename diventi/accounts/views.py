from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from braces.views import AnonymousRequiredMixin, LoginRequiredMixin

from .models import DiventiUser, DiventiAvatar
from .forms import DiventiUserCreationForm, DiventiUserUpdateForm
from diventi.core.views import DiventiActionMixin


class DiventiLoginView(AnonymousRequiredMixin, LoginView):

	template_name = "accounts/signin.html"


class DiventiLogoutView(LoginRequiredMixin, LogoutView):

	template_name = "accounts/signout.html"


@login_required(redirect_field_name='accounts:signin')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('landing:home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
    })


class DiventiUserCreationView(AnonymousRequiredMixin, CreateView):

    form_class = DiventiUserCreationForm
    model = DiventiUser
    template_name = 'accounts/signup.html'
    success_msg = 'You have signed up!'
    success_url = reverse_lazy('landing:home')
    fail_msg = 'Your sign-up has failed.'
    fail_url = reverse_lazy('accounts:signup')

    def form_valid(self, form):
        username = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        if username and password:
            form.save()
            user = get_object_or_404(DiventiUser, email=username)
            login(self.request, user)
            messages.success(self.request, self.success_msg)
            redirect(self.success_url)
        else:
            messages.error(self.request, self.fail_msg)
        return super(DiventiUserCreationView, self).form_valid(form)


class DiventiUserUpdateView(LoginRequiredMixin, DiventiActionMixin, UpdateView):

    form_class = DiventiUserUpdateForm
    model = DiventiUser
    template_name = "accounts/update.html"
    success_msg = 'Profile updated!'
    fail_msg = 'Profile has not been updated.'

    def get_form_kwargs(self):
        """ Inject form with additional keyword arguments."""
        kwargs = super(DiventiUserUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


