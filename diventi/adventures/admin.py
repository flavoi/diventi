from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin

from .models import (
    Adventure,
    Situation,
    Match,
    Story,
    Resolution,
)

from .forms import AdventureForm


class AdventureAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'ring', 'created']
    form = AdventureForm
    readonly_fields = ['created', 'modified']


class StoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'adventure', 'game_master', 'created', 'situation_tag']
    readonly_fields = ['created', 'modified']


class SituationAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'created']
    readonly_fields = ['created', 'modified']


class ResolutionAdmin(DiventiTranslationAdmin):
    fields = ('title', 'color', 'icon')


admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Situation, SituationAdmin)
admin.site.register(Match)
admin.site.register(Resolution, ResolutionAdmin)
admin.site.register(Story, StoryAdmin)