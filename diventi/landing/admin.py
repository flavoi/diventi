from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationTabularInline, TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, deactivate, make_published, make_unpublished

from .models import Presentation, Feature, Section
from .forms import PresentationForm, SectionForm


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'color', 'description',)
    extra = 0


class SectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'get_features', 'get_products', 'get_users', 'published', 'featured', 'featured_link']
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
        (_('Additionals'), {
            'fields': ('products', 'users',),
        }),
    )
    inlines = [        
        FeatureInline,
    ]
    actions = [make_published, make_unpublished]
    form = SectionForm
    ordering = ['-published', 'order_index']


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