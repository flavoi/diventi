from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin

from modeltranslation.admin import TranslationTabularInline

from .models import Presentation, Feature


class FeatureInline(TranslationTabularInline):
    model = Feature
    # fields = ('title', 'icon', 'color', 'description')
    # extra = 0


class PresentationAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'active']    
    inlines = [
        FeatureInline,
    ]

admin.site.register(Presentation, PresentationAdmin)