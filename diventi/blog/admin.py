from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished, deactivate

from .models import Article, ArticleCategory, BlogCover


class ArticleAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'category', 'image_tag', 'hot', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'hot')
        }),
        (_('Editing'), {
            'fields': ('title', 'category', 'image', 'publication_date', 'content', 'label', 'author', 'slug'),
        }),
    )
    actions = [make_published, make_unpublished]


class BlogCoverAdmin(DiventiTranslationAdmin):
    list_display= ('label', 'image_tag', 'active')
    actions = [deactivate]


class CategoryAdmin(DiventiTranslationAdmin):
    list_display = ('title',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, CategoryAdmin)
admin.site.register(BlogCover, BlogCoverAdmin)