import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView, RedirectView
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
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import AnonymousRequiredMixin

from diventi.core.views import DiventiActionMixin, StaffRequiredMixin
from diventi.products.models import Product
from diventi.comments.models import DiventiComment
from diventi.landing.models import Section

from .models import DiventiUser
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


class UserModalDataView(LoginRequiredMixin, View):
    """
    Restituisce il contenuto aggiornato del modale utente via AJAX
    eseguendo get_user_data solo al momento della richiesta.
    """
    def get(self, request, *args, **kwargs):
        user_data = get_user_data(request.user)
        
        html = render_to_string(
            'accounts/partials/_user_modal_content.html',
            {'authenticated_user_data': user_data, 'user': request.user},
            request=request
        )
        return JsonResponse({'html': html})


class DiventiLoginView(LoginView):

    authentication_form = DiventiAuthenticationForm
    form_class = DiventiAuthenticationForm
    template_name = "accounts/signin_quick.html"
    success_msg = _('You have signed in!')
    fail_msg = _('Your sign in has failed.')

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)        
        return super().form_valid(form)


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
    message_type = 'danger'

    if request.method == 'POST':
        form = DiventiPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantiene l'utente autenticato aggiornando l'hash della sessione
            update_session_auth_hash(request, user)
            
            message = _('Your password was successfully updated!')
            message_type = 'success'
        else:
            error_message = {
                str(form.fields[field].label or field) if field in form.fields else _('Error'): error 
                for field, error in form.errors.items()
            }
            message_type = 'danger'

    return JsonResponse({
        'message': str(message),
        'error_message': error_message,
        'message_type': message_type,
    })

@login_required
@csrf_protect
def change_privacy_ajax(request):
    """
    Updates user's privacy fields and returns the response as ajax.
    """
    message = ''
    error_message = ''
    message_type = 'danger'

    if request.method == 'POST':
        form = DiventiUserPrivacyChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            message = _('Your privacy was successfully updated!')
            message_type = 'success'
        else:
            error_message = {
                str(form.fields[field].label or field) if field in form.fields else _('Error'): error 
                for field, error in form.errors.items()
            }
            message_type = 'danger'

    return JsonResponse({
        'message': str(message),
        'error_message': error_message,
        'message_type': message_type,
    })


class DiventiUserCreationView(AnonymousRequiredMixin, CreateView):

    form_class = DiventiUserCreationForm
    model = DiventiUser
    template_name = 'accounts/signup_quick.html'
    success_msg = _('You have signed up!')
    fail_msg = _('Your sign up has failed.')
    fail_url = reverse_lazy('accounts:signup')

    def get_initial(self):
        # Retrieve initial data from user inputs on the landing page
        initial = super().get_initial()
        initial_email = self.request.session.get('initial_email', None)
        initial_first_name = self.request.session.get('initial_first_name', None)
        initial = {
            'email': initial_email,
            'first_name': initial_first_name,
        }
        return initial

    def get_success_url(self):
        self.request.session['show_login_form'] = 1
        next_path = self.request.GET.get('next', '')
        if next_path:
            return next_path
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
        return self.object.pk == self.request.user.pk

    def get_success_url(self):        
        return reverse('accounts:settings', kwargs={'nametag': self.object.nametag})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not self.user_passes_test():
            raise PermissionDenied(_("A user may update his own profile only."))
        return kwargs

    def form_valid(self, form):
        is_ajax = self.request.headers.get('x-requested-with') == 'XMLHttpRequest' or self.request.is_ajax()
        
        if is_ajax:
            # Salviamo il modello direttamente evitando DiventiActionMixin / messages.success
            self.object = form.save()
            
            changed_fields = form.changed_data
            if changed_fields:
                labels = [
                    str(form.fields[f].label or f).lower() 
                    for f in changed_fields 
                    if f in form.fields
                ]
                msg = _('Updated successfully: %(fields)s') % {'fields': ', '.join(labels)}
            else:
                msg = str(self.success_msg)

            return JsonResponse({
                'message_type': 'success',
                'message': msg,
                'nametag': self.object.nametag,
                'redirect_url': self.get_success_url(),
            })
            
        return super().form_valid(form)

    def form_invalid(self, form):
        is_ajax = self.request.headers.get('x-requested-with') == 'XMLHttpRequest' or self.request.is_ajax()
        
        if is_ajax:
            error_message = {
                str(form.fields[field].label or field) if field in form.fields else _('Error'): error 
                for field, error in form.errors.items()
            }
            return JsonResponse({
                'message_type': 'danger',
                'message': str(self.fail_msg),
                'error_message': error_message,
            })
            
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = get_user_data(self.object)
        return context
        

class DiventiUserPasswordChangeView(LoginRequiredMixin, DiventiActionMixin, PasswordChangeView):

    model = DiventiUser
    form_class = DiventiPasswordChangeForm
    template_name = "accounts/user_change_password_quick.html"

    def user_passes_test(self, requested_user):
        """ A user may update his own profile only. """
        if requested_user.pk == self.request.user.pk:
            return 1            
        return 0
    
    def dispatch(self, *args, **kwargs):        
        requested_user = get_object_or_404(DiventiUser, nametag=kwargs['nametag'])
        if not self.user_passes_test(requested_user):
            raise PermissionDenied(_("A user may update his own profile only."))
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """ If we're here we assume the user is changing his own password """
        context = super().get_context_data(**kwargs)
        context.update(
            {"object": self.request.user}
        )
        return context


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

    def get_queryset(self):
        return super().get_queryset().prefetch()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = get_user_data(self.object, self)
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
        
        # Carichiamo tutti gli utenti attivi in un'unica query
        all_users = list(DiventiUser.objects.is_active())
        subscribers = [u for u in all_users if u.has_agreed_gdpr]
        
        # Raggruppiamo in RAM senza rieseguire .filter() su DB per ogni lingua
        users_lan = {}
        for user in all_users:
            users_lan.setdefault(user.language, []).append(user)
            
        subscribers_lan = {}
        for sub in subscribers:
            subscribers_lan.setdefault(sub.language, []).append(sub)

        context['users_count'] = len(all_users)
        context['users_lan'] = users_lan
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


class DiventiUserDetailRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(DiventiUser, pk=kwargs['pk'])
        return reverse_lazy('accounts:detail', args=(user.nametag,))


    