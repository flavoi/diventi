from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin

from .models import (
    Adventure,
    Situation,
    Match,
    Story,
)

from .forms import AdventureForm


class AdventureAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'ring', 'created']
    form = AdventureForm
    readonly_fields = ['created', 'modified']


class StoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'adventure', 'game_master', 'created']
    readonly_fields = ['created', 'modified']


class SituationAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'adventure', 'created']
    readonly_fields = ['created', 'modified']


admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Situation, SituationAdmin)
admin.site.register(Match)
admin.site.register(Story, StoryAdmin)