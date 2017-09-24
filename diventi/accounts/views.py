from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


class DiventiLoginView(LoginView):

	template_name = "accounts/login.html"


class DiventiLogoutView(LogoutView):

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