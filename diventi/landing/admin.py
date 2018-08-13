from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import Presentation, Feature, Feedback, About


class AboutInline(TranslationStackedInline):
    model = About
    fields = ('title', 'description')
    extra = 0


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description')
    extra = 0


class PresentationAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'active']    
    inlines = [        
        AboutInline,
        FeatureInline,
    ]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created', 'modified']


admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Feedback, FeedbackAdmin)