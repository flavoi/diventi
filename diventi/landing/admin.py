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
    list_display = ['title', 'image_tag', 'order_index', 'get_features', 'get_products', 'get_users', 'section_survey', 'published', 'featured',]
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured')
        }),
        (_('Templates'), {
            'fields': ('template', 'featured_template')
        }),
        (_('Editing'), {
            'fields': ('title', 'abstract', 'order_index', 'description', 'image'),
        }),
        (_('Additionals'), {
            'fields': ('products', 'users', 'section_survey'),
        }),
    )
    inlines = [        
        FeatureInline,
    ]
    actions = [make_published, make_unpublished]
    form = SectionForm
    ordering = ['-published', 'order_index']
    

admin.site.register(Section, SectionAdmin)