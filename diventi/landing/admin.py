from django.contrib import admin

from diventi.core.admin import DiventiTranslationAdmin

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from .models import Presentation, Feature, Feedback, FeaturesCover


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description')
    extra = 0


class FeaturesCoverAdmin(DiventiTranslationAdmin):
    list_display= ('label', 'image_tag')


class PresentationAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'active']    
    inlines = [
        FeatureInline,
    ]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',]


admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeaturesCover, FeaturesCoverAdmin)