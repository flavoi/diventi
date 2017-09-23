from django.contrib import admin

from .models import Profile, Feature


class FeatureInline(admin.TabularInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']    
    inlines = [
        FeatureInline,
    ]


admin.site.register(Profile, ProfileAdmin)