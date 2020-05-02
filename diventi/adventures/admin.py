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
    fields = ('title', 'color', 'icon')


class AntagonistAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag']
    fields = ('title', 'image')


class AntagonistGoalAdmin(DiventiTranslationAdmin):
    list_display = ['antagonist', 'title', 'level', 'adventure', 'icon_tag']
    ordering = ('antagonist', 'level')
    fields = ('title', 'description', 'level', 'adventure', 'antagonist', 'icon')


admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Situation, SituationAdmin)
admin.site.register(Match)
admin.site.register(Resolution, ResolutionAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Antagonist, AntagonistAdmin)
admin.site.register(AntagonistGoal, AntagonistGoalAdmin)