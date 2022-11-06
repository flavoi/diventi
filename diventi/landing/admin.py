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
)
from .forms import SectionForm


class FeatureInline(TranslationStackedInline):
    model = Feature
    fields = ('title', 'icon', 'icon_style', 'color', 'description',)
    extra = 0


class SectionAdmin(DiventiTranslationAdmin):
    list_display = [
        'title', 
        'image_tag',
        'video_image_tag',
        'order_index',
        'featured_video',
        'published',
        'featured',
    ]
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured')
        }),
        (_('Multimedia'), {
            'fields': ('image', 'video', 'video_label', 'video_image', 'featured_video')
        }),
        (_('Editing'), {
            'fields': ('order_index', 'prefix', 'title', 'button_label', 'description',),
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