from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline, TranslationTabularInline

from diventi.core.admin import DiventiTranslationAdmin

from .models import CharacterSheet, Relationship


class RelationshipInline(TranslationStackedInline):
    model = Relationship
    fields = ['title', 'description']
    extra = 0


class CharacterSheetAdmin(DiventiTranslationAdmin):
    list_display = ['name', 'origin', 'predisposition', 'book']
    fieldsets = (
        (_('Management'), {
            'fields': ('book', 'player')
        }),
        (_('Editing'), {
            'fields': ('name', 'origin', 'predisposition', 'slug'),
        }),
    )
    inlines = (RelationshipInline,)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(CharacterSheet, CharacterSheetAdmin)
admin.site.register(Relationship)