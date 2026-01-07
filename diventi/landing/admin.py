from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from modeltranslation.admin import (
    TranslationTabularInline, 
    TranslationStackedInline,
)

from diventi.core.admin import (
    DiventiTranslationAdmin,
    DiventiIconAdmin,
    deactivate, 
    make_published, 
    make_unpublished,
)

from diventi.products.models import Product

from .models import (
    Feature, 
    Section,
    SearchSuggestion,
    AboutArticle,
    SectionImage,
    LandingPage,
)
from .forms import SectionForm


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'prefix', 'subtitle', 'icon', 'color', 'description',)
    extra = 0


class SectionAdmin(DiventiTranslationAdmin):
    list_display = [
        'title',
        'featured',
        'subtitle',
        'video_image_tag',
        'cover_primary_tag',
        'cover_secondary',
        'order_index',
    ]
    fieldsets = (
        (_('Management'), {
            'fields': ('featured',)
        }),
        (_('Multimedia'), {
            'fields': ('video', 'video_image','cover_primary', 'cover_secondary')
        }),
        (_('Editing'), {
            'fields': ('order_index', 'prefix', 'title', 'subtitle', 'short_description', 'button_label', 'description', 'slug'),
        }),
        (_('Attachments'), {
            'fields': ('attached_product', 'attached_section'),
        }),
    )
    inlines = [        
        FeatureInline,
    ]
    actions = [make_published, make_unpublished]
    form = SectionForm
    list_filter = ['landing_pages',]
    ordering = ['-featured', 'order_index']
    prepopulated_fields = {"slug": ("title",)}

    def cover_primary_tag(self, obj):
        if obj.cover_primary:
            return obj.cover_primary.image_tag()
        else:
            return '-'
    cover_primary_tag.short_description = _('primary cover')

    def get_form(self, request, obj=None, **kwargs):
        form = super(SectionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['attached_product'].queryset = Product.objects.filter(published=True)
        return form


class SearchSuggestionAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    list_display = ('title', 'icon_tag', 'description',)
    fields = ('title', 'icon', 'description',)


class AboutArticleAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'get_hitcounts', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (_('Management'), {
            'fields': ('published',)
        }),
        (_('Editing'), {
            'fields': ('title', 'description', 'content', 'slug', 'publication_date'),
        }),
    )
    actions = [make_published, make_unpublished]


class LandingPageAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'featured', 'published', 'enable_pinned_content', 'enable_signin', ]
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured'),
        }),
        (_('Content'), {
            'fields': ('enable_pinned_content', 'enable_signin', 'sections', ),
        }),
        (_('Editing'), {
            'fields': ('title', 'description', 'theme', 'slug', 'publication_date'),
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_published, make_unpublished]

    def get_form(self, request, obj=None, **kwargs):
        form = super(LandingPageAdmin, self).get_form(request, obj, **kwargs)
        queryset = Section.objects.filter(
            Q(landing_pages=obj) | Q(landing_pages__isnull=True)
        ).filter(section__isnull=True)
        form.base_fields['sections'].queryset = queryset
        return form


admin.site.register(Section, SectionAdmin)
admin.site.register(SearchSuggestion, SearchSuggestionAdmin)
admin.site.register(AboutArticle, AboutArticleAdmin)
admin.site.register(SectionImage)
admin.site.register(LandingPage, LandingPageAdmin)