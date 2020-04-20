from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from diventi.ebooks.models import (
    Section,
)
from .models import (
    Story,
    Situation,
    Resolution,
    Match,
)

from .forms import(
    SituationCreateForm,
)


class StorySituationCreateView(LoginRequiredMixin, CreateView):

    form_class = SituationCreateForm
    model = Situation
    template_name = 'adventures/new_game.html'
    success_msg = _('You have started a new game!')
    fail_msg = _('An error was found while creating you game.')
    fail_url = reverse_lazy('adventures:new-game')

    def form_valid(self, form):
        form.instance.game_master = self.request.user
        adventure = form.cleaned_data['adventure']
        form.instance.story = Story.objects.create()
        messages.success(self.request, self.success_msg)  
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_situations = Situation.objects.gm_situations(game_master=self.request.user, exclude_situation=self.object)
        context['user_situations'] = user_situations
        return context


class SituationDetailView(LoginRequiredMixin, DetailView):

    model = Situation
    context_object_name = 'situation'
    slug_field = 'story'
    slug_url_kwarg = 'uuid'

    # Returns the situation if the game master is staff or the current user
    def get_queryset(self):
        qs = super(SituationDetailView, self).get_queryset()
        user = self.request.user
        return qs.game_master(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resolutions'] = Resolution.objects.all()
        return context


def get_story(request, story_uuid):
    is_user_game_master = Situation.objects.filter(story__uuid=story_uuid, game_master=request.user).exists()
    if is_user_game_master:
        messages.info(request, _('Hi game master, you are viewing the players\' page.')) 
    elif self.request.user.is_authenticated:
       match = Match.objects.get_or_create(situation=self.object, player=request.user)
       messages.success(request, _('You have joined a new game.'))
    return HttpResponseRedirect(reverse('adventures:story_detail', args=[story_uuid,]))


class StoryDetailView(DetailView):

    model = Story
    context_object_name = 'story'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        situation = get_object_or_404(Situation, story=self.object.uuid)
        section = Section.objects.filter(pk=situation.adventure.section.pk)
        section = section.usection()
        context['section'] = section.get()
        context['situation'] = situation
        return context


class LandingView(LoginRequiredMixin, TemplateView):

    template_name = "adventures/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add data here
        return context


# Story navigation algorithm
def situation_next(request, current_story_uuid):
    return HttpResponseRedirect(reverse('adventures:story_detail', args=[current_story_uuid,]))