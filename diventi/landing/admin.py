from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin, deactivate

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import Presentation, Feature


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description',)
    extra = 0


class PresentationAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'active']    
    inlines = [        
        FeatureInline,
    ]

admin.site.register(Presentation, PresentationAdmin)