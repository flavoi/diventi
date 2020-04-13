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
    list_display = ['title', 'ring']
    form = AdventureForm

admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Situation)
admin.site.register(Match)
admin.site.register(Story)