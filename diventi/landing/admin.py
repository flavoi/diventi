from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

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
)
from .forms import SectionForm


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'icon_style', 'color', 'description',)
    extra = 0

class SectionAdmin(DiventiTranslationAdmin):
    list_display = [
        'title',
        'subtitle',
        'image_tag',
        'video_image_tag',
        'get_cover_primary_tag',
        'get_cover_secondary_tag',
        'order_index',
        'published',
        'featured',
    ]
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured')
        }),
        (_('Multimedia'), {
            'fields': ('image', 'video', 'video_image','cover_primary', 'cover_secondary')
        }),
        (_('Editing'), {
            'fields': ('order_index', 'prefix', 'title', 'subtitle', 'button_label', 'description',),
        }),
        (_('Attachments'), {
            'fields': ('attachment_label', 'attached_product',),
        }),
    )
    inlines = [        
        FeatureInline,
    ]
    actions = [make_published, make_unpublished]
    form = SectionForm
    ordering = ['-featured', 'order_index']

    def get_cover_primary_tag(self, obj):
        if obj.cover_primary:
            return obj.cover_primary.image_tag()
        else:
            return '-'
    get_cover_primary_tag.short_description = _('primary cover')

    def get_cover_secondary_tag(self, obj):
        if obj.cover_secondary:
            return obj.cover_secondary.image_tag()
        else:
            return '-'
    get_cover_secondary_tag.short_description = _('secondary cover')

    def get_form(self, request, obj=None, **kwargs):
        form = super(SectionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['attached_product'].queryset = Product.objects.filter(published=True)
        return form


class SearchSuggestionAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    list_display = ('title', 'icon_tag', 'description',)
    fields = ('title', 'icon', 'description',)


class GenericArticleAdmin(DiventiTranslationAdmin):
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


admin.site.register(Section, SectionAdmin)
admin.site.register(SearchSuggestion, SearchSuggestionAdmin)
admin.site.register(AboutArticle, GenericArticleAdmin)
admin.site.register(SectionImage)