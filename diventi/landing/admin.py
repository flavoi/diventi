from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin, deactivate

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import Presentation, Feature, Feedback, About, AboutCover


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



class AboutCoverAdmin(DiventiTranslationAdmin):
    list_display= ('label', 'image_tag', 'active')
    actions = [deactivate]
    

admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(AboutCover, AboutCoverAdmin)