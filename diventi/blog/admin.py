from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import (
    DiventiTranslationAdmin,
    DiventiIconAdmin,
    make_published,
    make_unpublished,
    deactivate,
)

from .models import (
    Article, 
    ArticleCategory, 
    BlogCover,
)

from .forms import ArticleForm


class ArticleAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    list_display = ['title', 'category','image_tag', 'postcard_tag', 'get_hitcounts', 'get_readtime', 'hot', 'published', 'publication_date', 'created']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'hot')
        }),
        (_('Layout'), {
            'fields': ('col_lg', 'col_md')
        }),
        (_('Multimedia'), {
            'fields': ('image', 'postcard'),
        }),
        (_('Editing'), {
            'fields': ('title', 'category', 'description', 'content', 'label', 'author', 'slug', 'publication_date'),
        }),
        (_('Related'), {
            'fields': ('related_articles',),
        }),
    )
    form = ArticleForm
    actions = [make_published, make_unpublished]
    list_filter = ('category',)
    ordering = ('-created','publication_date',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)
        form.author_field = 'author'
        return form


class BlogCoverAdmin(DiventiTranslationAdmin):
    list_display= ('title', 'description', 'image_tag', 'active')
    fieldsets = (
        (_('Management'), {
            'fields': ('active',)
        }),
        (_('Editing'), {
            'fields': ('title', 'image', 'description',),
        }),
    )
    actions = [deactivate]


class CategoryAdmin(DiventiTranslationAdmin, DiventiIconAdmin):
    list_display = ('title', 'color_tag')
    fieldsets = (
        (_('Editing'), {
            'fields': ('title',),
        }),
        (_('Visual style'), {
            'fields': ('color',),
        }),
    )

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, CategoryAdmin)
admin.site.register(BlogCover, BlogCoverAdmin)