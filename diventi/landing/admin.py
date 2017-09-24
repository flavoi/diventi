from django.contrib import admin

from .models import Presentation, Feature


class FeatureInline(admin.TabularInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description')


class PresentationAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']    
    inlines = [
        FeatureInline,
    ]


admin.site.register(Presentation, PresentationAdmin)