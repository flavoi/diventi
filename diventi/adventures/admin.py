from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin

from .models import (
    Adventure,
    Situation,
    Match,
    Story,
    Resolution,
    Antagonist,
    AntagonistGoal,
)

from .forms import AdventureForm


class AdventureAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'ring', 'created']
    form = AdventureForm
    readonly_fields = ['created', 'modified']


class SituationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'adventure', 'resolution', 'game_master', 'created', 'story_tag']
    readonly_fields = ['created', 'modified']


class StoryAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'navigation', 'created']
    readonly_fields = ['created', 'modified']


class ResolutionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'get_antagonist_goals', 'story_points',]
    fields = ('title', 'antagonist_goals', 'story_points')


class AntagonistAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag']
    fields = ('title', 'image')


class AntagonistGoalAdmin(DiventiTranslationAdmin):
    list_display = ['subject', 'icon_tag']
    ordering = ('antagonist',)
    fields = ('title', 'description', 'antagonist', 'icon', 'subject')
    readonly_fields = ['subject']

