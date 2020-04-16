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
        game_master = self.request.user
        story_already_created = Story.objects.filter(game_master=game_master, resolution='')
        if story_already_created.exists():
            msg = _('We have redirected you to your ongoing adventure.')
            story_already_created = story_already_created.first()
            messages.info(self.request, msg)
            return HttpResponseRedirect(reverse('adventures:story_detail', args=[story_already_created.pk,]))
        form.instance.game_master = game_master
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


class LandingView(LoginRequiredMixin, TemplateView):

    template_name = "adventures/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add data here
        return context

