from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, deactivate

from .models import Presentation, Feature, Section
from .forms import PresentationForm


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description',)
    extra = 0


class SectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'description']
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured')
        }),
        (_('Templates'), {
            'fields': ('template', 'featured_template')
        }),
        (_('Editing'), {
            'fields': ('title', 'abstract', 'order_index', 'presentation', 'description',),
        }),
    )
    inlines = [        
        FeatureInline,
    ]
    actions = [deactivate]


class PresentationAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'featured_link', 'active']
    fieldsets = (
        (_('Management'), {
            'fields': ('active', 'template',)
        }),
        (_('Editing'), {
            'fields': ('title', 'image', 'featured_link', 'featured_label', 'abstract', 'description', 'projects_description'),
        }),
    )  
    inlines = [        
        FeatureInline,
    ]
    actions = [deactivate]
    form = PresentationForm

admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Section, SectionAdmin)