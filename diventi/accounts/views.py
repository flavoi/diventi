from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from braces.views import AnonymousRequiredMixin, LoginRequiredMixin

from .models import DiventiUser, DiventiAvatar
from .forms import DiventiUserCreationForm, DiventiUserUpdateForm
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
        self.request.session['fail_login_msg'] = self.fail_msg        
        return redirect(self.fail_url)
        

class DiventiLogoutView(LoginRequiredMixin, LogoutView):

	template_name = "accounts/signout.html"


@login_required(redirect_field_name='accounts:signin')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Your password was successfully updated!'))
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
    success_msg = _('You have signed up!')    
    fail_msg = _('Your sign up has failed.')
    fail_url = reverse_lazy('accounts:signup')

    def get_initial(self):
        # Retrieve initial data from user inputs on the landing page
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

    def form_valid(self, form):
        username = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        if username and password:
            form.save()
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                messages.success(self.request, self.success_msg)
                return redirect(self.get_success_url())
            else:
                messages.error(self.request, self.fail_msg)
        return super(DiventiUserCreationView, self).form_valid(form)


class DiventiUserUpdateView(LoginRequiredMixin, DiventiActionMixin, UpdateView):

    form_class = DiventiUserUpdateForm
    model = DiventiUser
    template_name = "accounts/profile.html"
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
        user = self.request.user
        kwargs['user'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DiventiUserUpdateView, self).get_context_data(**kwargs)
        collection = Product.objects.user_collection(user=self.request.user)
        context['collection'] = collection
        return context



