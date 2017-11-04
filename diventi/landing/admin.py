from django.contrib import admin

from .models import Presentation, Feature, Event


class FeatureInline(admin.TabularInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description')
    extra = 0


class EventInline(admin.TabularInline):
    model = Event
    fields = ('title', 'icon', 'color', 'description', 'event_date')
    extra = 0


class PresentationAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']    
    inlines = [
        FeatureInline,
        EventInline,
    ]

admin.site.register(Presentation, PresentationAdmin)