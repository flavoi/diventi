from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Presentation, Feature


class FeatureInline(admin.TabularInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description')
    extra = 0


class PresentationAdmin(TranslationAdmin):
    list_display = ['pk', 'title', 'active']    
    inlines = [
        FeatureInline,
    ]

admin.site.register(Presentation, PresentationAdmin)