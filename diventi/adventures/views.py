from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, FormView
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
    Adventure,
    Story,
    Situation,
    Resolution,
    Match,
)

from .forms import(
    SituationCreateForm,
    AdventureNavigationForm,
)


class SituationStoryCreateView(LoginRequiredMixin, CreateView):

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
        user_situations = Situation.objects.open(game_master=self.request.user, exclude_situation=self.object)
        context['user_situations'] = user_situations
        return context


class SituationDetailView(LoginRequiredMixin, DetailView):
    model = Situation
    context_object_name = 'situation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resolutions'] = Resolution.objects.all()
        context['adventure_navigation_form'] = AdventureNavigationForm()
        return context


class SituationStoryDetailView(SituationDetailView):

    slug_field = 'story'
    slug_url_kwarg = 'uuid'

    # Returns the last situation of the story 
    # if the game master is staff or the current user
    def get_queryset(self):
        user = self.request.user
        last_situation_of_story = Situation.objects.filter(story=self.kwargs['uuid'])
        last_situation_of_story = last_situation_of_story.game_master(user)
        last_situation_of_story = last_situation_of_story.order_by('-pk').first()
        qs = Situation.objects.filter(pk=last_situation_of_story.pk)
        return qs


def story_get(request, uuid):
    is_user_game_master = Situation.objects.filter(story__uuid=uuid, game_master=request.user).exists()
    if is_user_game_master:
        messages.info(request, _('Hi game master, you are viewing the players\' page.')) 
    elif self.request.user.is_authenticated:
       match = Match.objects.get_or_create(situation=self.object, player=request.user)
       messages.success(request, _('You have joined a new game.'))
    return HttpResponseRedirect(reverse('adventures:story_detail', args=[uuid,]))


class StoryDetailView(DetailView):

    model = Story
    context_object_name = 'story'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        situation = Situation.objects.current(self.object.uuid)
        section = Section.objects.filter(pk=situation.adventure.section.pk)
        section = section.usection()
        context['section'] = section.get()
        context['situation'] = situation
        return context


class SituationStoryResolutionView(FormView):

    template_name = 'adventures/situation_detail.html'
    form_class = AdventureNavigationForm

    def get_context_data(self, **kwargs):
        if 'situation' not in kwargs:
            kwargs['situation'] = Situation.objects.current(self.kwargs['uuid'])
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # Redirect the navigation according to game master preference
        current_situation = Situation.objects.current(self.kwargs['uuid'])
        current_situation.resolution = form.cleaned_data['resolution']
        current_situation.save()
        next_situation, created = situation_random(
            self.request, 
            current_situation=current_situation,
            enable_third_ring=form.cleaned_data['enable_third_ring'],
        )
        if current_situation != next_situation:
            messages.info(
                self.request, 
                _('You have unlocked a situation of the {ring}.'.format(ring=next_situation.adventure.get_ring_display().lower()))
            )
        return HttpResponseRedirect(reverse('adventures:situation_detail', args=[next_situation.story.uuid,]))


# Default navigation:
# A loop of random second rings adventure
def situation_random(request, current_situation, enable_third_ring=None):
    story = get_object_or_404(Story, uuid=current_situation.story.uuid)
    adventure = Adventure.objects.random_second_ring()
    third_ring = Adventure.objects.third_ring()
    if enable_third_ring and third_ring:
        next_situation = Situation.objects.get_or_create(
            adventure=third_ring, 
            story=story, 
            game_master=current_situation.game_master,
        )
    elif adventure:
        next_situation = Situation.objects.get_or_create(
            adventure=adventure, 
            story=story, 
            game_master=current_situation.game_master,
        )       
    else:
        next_situation = current_situation
    return next_situation