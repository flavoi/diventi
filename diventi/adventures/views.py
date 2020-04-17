from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import (
    Story,
    Situation,
)

from .forms import(
    StoryCreateForm,
)


class StorySituationCreateView(LoginRequiredMixin, CreateView):

    form_class = StoryCreateForm
    model = Story
    template_name = 'adventures/new_game.html'
    success_msg = _('You have started a new game!')
    fail_msg = _('An error was found while creating you game.')
    fail_url = reverse_lazy('adventures:new-game')

    def form_valid(self, form):
        form.instance.game_master = self.request.user
        adventure = form.cleaned_data['adventure']
        Situation.objects.create(adventure=adventure)
        messages.success(self.request, self.success_msg)  
        return super().form_valid(form)


class StoryDetailView(LoginRequiredMixin, DetailView):

    model = Story
    context_object_name = 'story'

    # Returns the story if the game master is staff or the current user
    def get_queryset(self):
        qs = super(StoryDetailView, self).get_queryset()
        user = self.request.user
        return qs.game_master(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_stories = Story.objects.stories(game_master=self.request.user, exclude_story=self.object)
        context['user_stories'] = user_stories
        return context


class LandingView(LoginRequiredMixin, TemplateView):

    template_name = "adventures/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add data here
        return context

