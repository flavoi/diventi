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

from .models import (
    Feature, 
    Section,
    SearchSuggestion,
    AboutArticle,
    PolicyArticle,
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
        'order_index', 
        'published', 
        'featured',
    ]
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured')
        }),
        (_('Multimedia'), {
            'fields': ('image', 'video',)
        }),
        (_('Layout'), {
            'fields': ('alignment', 'position',),
        }),
        (_('Editing'), {
            'fields': ('prefix', 'title', 'button_label', 'order_index', 'description',),
        }),
        (_('Attachment'), {
            'fields': ('about_article', 'product_category', 'article_category',),
        }),
    )
    inlines = [        
        FeatureInline,
    ]
    actions = [make_published, make_unpublished]
    form = SectionForm
    ordering = ['-featured', 'order_index']


class SearchSuggestionAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    list_display = ('title', 'icon_tag', 'description',)
    fields = ('title', 'icon', 'description',)


class GenericArticleAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    fieldsets = (
        (_('Management'), {
            'fields': ('published',)
        }),
        (_('Editing'), {
            'fields': ('title', 'content', 'slug', 'publication_date'),
        }),
    )
    actions = [make_published, make_unpublished]


admin.site.register(Section, SectionAdmin)
admin.site.register(SearchSuggestion, SearchSuggestionAdmin)
admin.site.register(AboutArticle, GenericArticleAdmin)
admin.site.register(PolicyArticle, GenericArticleAdmin)