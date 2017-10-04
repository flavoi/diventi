from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from braces.views import AnonymousRequiredMixin, LoginRequiredMixin

from .models import DiventiUser
from .forms import DiventiUserCreationForm


class DiventiLoginView(AnonymousRequiredMixin, LoginView):

	template_name = "accounts/login.html"


class DiventiLogoutView(LoginRequiredMixin, LogoutView):

	template_name = "accounts/logout.html"


@login_required(redirect_field_name='accounts:login')
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
        password = form.cleaned_data['password']
        if username and password:
            form.save()
            user = get_object_or_404(DiventiUser, email=username)
            login(self.request, user)
            messages.success(self.request, self.success_msg)
            redirect(self.success_url)
        else:
            messages.error(self.request, self.fail_msg)
        return super(DiventiUserCreationView, self).form_valid(form)




