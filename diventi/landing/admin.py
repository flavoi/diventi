from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import (
    TranslationTabularInline, 
    TranslationStackedInline,
)

from diventi.core.admin import DiventiTranslationAdmin, deactivate, make_published, make_unpublished

from .models import (
    Feature, 
    Section,
    Story,
    SearchSuggestion
)
from .forms import SectionForm


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description',)
    extra = 0


class StoryInline(TranslationStackedInline):
    model = Story
    fields = ('title', 'icon', 'color', 'description', 'image')
    extra = 0


class SectionAdmin(DiventiTranslationAdmin):
    list_display = [
        'title', 
        'image_tag', 
        'order_index', 
        'get_features', 
        'get_products', 
        'get_users', 
        'get_articles', 
        'get_stories', 
        'section_survey', 
        'published', 
        'featured',
    ]
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured')
        }),
        (_('Visual style'), {
            'fields': ('template', 'featured_template', 'alignment', 'image', 'dark_mode',)
        }),
        (_('Editing'), {
            'fields': ('title', 'order_index', 'description',),
        }),
        (_('Additionals'), {
            'fields': ('video', 'products', 'users', 'section_survey', 'articles',),
        }),
    )
    inlines = [        
        FeatureInline,
        StoryInline,
    ]
    actions = [make_published, make_unpublished]
    form = SectionForm
    ordering = ['-featured', 'order_index']


class SearchSuggestionAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'icon_tag', 'description',)
    fields = ('title', 'icon', 'description',)

    class Media:
        js = ('https://kit.fontawesome.com/27968f469b.js', )


admin.site.register(Section, SectionAdmin)
admin.site.register(SearchSuggestion, SearchSuggestionAdmin)