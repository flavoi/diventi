from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .models import (
    Story,
    Situation,
)

from .forms import(
    SituationCreateForm,
)


class StorySituationCreateView(LoginRequiredMixin, CreateView):

    form_class = SituationCreateForm
    model = Story
    template_name = 'adventures/new_game.html'
    success_msg = _('You have signed up!')
    fail_msg = _('Your sign up has failed.')
    fail_url = reverse_lazy('adventures:signup')

    def get_success_url(self):
        return reverse_lazy('adventures:landing')

    def form_valid(self, form):
        game_master = self.request.user
        adventure = form.cleaned_data['adventure']
        Story.objects.create(game_master=game_master, adventure=adventure)
        return super().form_valid(form)


class LandingView(LoginRequiredMixin, TemplateView):

    template_name = "adventures/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add data here
        return context

