from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished, deactivate

from .models import Article, ArticleCategory, BlogCover
from .forms import ArticleForm


class ArticleAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'category', 'image_tag', 'hot', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'hot')
        }),
        (_('Layout'), {
            'fields': ('col_lg', 'col_md')
        }),
        (_('Editing'), {
            'fields': ('title', 'category', 'image', 'description', 'content', 'label', 'author', 'slug', 'publication_date'),
        }),
    )
    form = ArticleForm
    actions = [make_published, make_unpublished]

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


class CategoryAdmin(DiventiTranslationAdmin):
    list_display = ('title',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, CategoryAdmin)
admin.site.register(BlogCover, BlogCoverAdmin)