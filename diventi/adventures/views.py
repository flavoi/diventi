import sys

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
    SectionAspect,
    Secret,
)
from .models import (
    Adventure,
    Story,
    Situation,
    Resolution,
    Match,
    AntagonistGoal,
)

from .forms import(
    SituationCreateForm,
    SituationStoryResolutionForm,
)


class SituationStoryCreateView(LoginRequiredMixin, CreateView):

    form_class = SituationCreateForm
    model = Situation
    template_name = 'adventures/situation_story_create.html'
    success_msg = _('You have started a new game!')
    fail_msg = _('An error was found while creating you game.')
    fail_url = reverse_lazy('adventures:situation_story_create')

    def form_valid(self, form):
        form.instance.game_master = self.request.user
        adventure = form.cleaned_data['adventure']
        navigation = form.cleaned_data['navigation']
        form.instance.story = Story.objects.create(navigation=navigation)
        messages.success(self.request, self.success_msg)  
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_situations = Situation.objects.open(game_master=self.request.user)
        past_situations = Situation.objects.resolved(game_master=self.request.user)
        past_situations_uuids = past_situations.values_list('story__uuid')
        past_stories = Story.objects.filter(uuid__in=past_situations_uuids)
        past_stories = past_stories.prefetch_related('situations').prefetch_related('situations__adventure')
        context['open_situations'] = open_situations
        context['past_stories'] = past_stories
        return context


class SituationDetailView(LoginRequiredMixin, DetailView):
    model = Situation
    context_object_name = 'situation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.object.resolution:
            context['resolutions'] = Resolution.objects.all()
            context['adventure_navigation_form'] = SituationStoryResolutionForm(ring=self.object.adventure.ring)
        context['section'] = Section.objects.filter(pk=self.object.adventure.section.pk).usection().get()
        context['antagonist_goals'] = AntagonistGoal.objects.filter(adventure=self.object.adventure).prefetch()
        return context


class SituationStoryDetailView(SituationDetailView):

    template_name = 'adventures/situation_story_detail.html'
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
        context['antagonist_goals'] = AntagonistGoal.objects.filter(adventure=situation.adventure).prefetch()
        return context


class SituationStoryResolutionView(FormView):

    template_name = 'adventures/situation_detail.html'
    form_class = SituationStoryResolutionForm

    def get_context_data(self, **kwargs):
        if 'situation' not in kwargs:
            kwargs['situation'] = Situation.objects.current(self.kwargs['uuid'])
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # Redirect the navigation according to game master preference
        current_situation = Situation.objects.current(self.kwargs['uuid'])
        current_story = get_object_or_404(Story, uuid=current_situation.story.uuid)
        current_situation.resolution = form.cleaned_data['resolution']
        current_situation.save()
        adventures_already_played = Situation.objects.history(game_master=current_situation.game_master)
        adventures_already_played = adventures_already_played.filter(story__uuid=current_situation.story.uuid)
        if current_situation.adventure.ring == 'third':
            # Game master resolves a third ring adventure
            next_situation = current_situation
            messages.success(
                self.request, 
                _('You have completed the adventure "{adventure}"!'.format(adventure=current_situation.adventure.product))
            )
            return HttpResponseRedirect(reverse('adventures:situation_story_create'))
        else:
            # Available navigations:
            # - Exploration > situation_random
            next_situation, created = getattr(self, current_story.navigation)(
                current_situation=current_situation,
                adventures_already_played=adventures_already_played,
                enable_third_ring=form.cleaned_data['enable_third_ring'],
            )
        if current_situation != next_situation:
            messages.success(
                self.request, 
                _('You have unlocked a situation of the {ring}.'.format(ring=next_situation.adventure.get_ring_display().lower()))
            )
        return HttpResponseRedirect(reverse('adventures:situation_story_detail', args=[next_situation.story.uuid,]))


    # Default navigation:
    # A loop of random second rings adventure
    def situation_random(self, current_situation, adventures_already_played=None, enable_third_ring=None):
        if adventures_already_played:
            adventures_already_played_ids = adventures_already_played.values_list('adventure', flat=True)
        story = get_object_or_404(Story, uuid=current_situation.story.uuid)
        second_ring = Adventure.objects.random_second_ring(exclude_ids=adventures_already_played_ids)
        third_ring = Adventure.objects.third_ring()
        if enable_third_ring and third_ring:
            # Game master forces the third ring.
            next_situation = Situation.objects.get_or_create(
                adventure=third_ring, 
                story=story, 
                game_master=current_situation.game_master,
            )
        elif second_ring:
            # Game master resolves a second ring adventure.
            next_situation = Situation.objects.get_or_create(
                adventure=second_ring, 
                story=story, 
                game_master=current_situation.game_master,
            )       
        elif third_ring:
            # Game master resolves a second ring adventure
            # but there is only the conclusion left to be played.
            next_situation = Situation.objects.get_or_create(
                adventure=third_ring, 
                story=story, 
                game_master=current_situation.game_master,
            )
        else:
            # Game master resolves a second ring adventure
            # but there are no other situations to be played.
            next_situation = current_situation        
        return next_situation