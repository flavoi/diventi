from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from .models import Article, ArticleCategory, BlogCover


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected stories as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected stories as hidden")


def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)
deactivate.short_description = _("Mark selected covers for deactivation")


class ArticleAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'category', 'hot', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    actions = [make_published, make_unpublished]


class BlogCoverAdmin(DiventiTranslationAdmin):
    list_display= ('label', 'image_tag', 'active')
    actions = [deactivate]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory)
admin.site.register(BlogCover, BlogCoverAdmin)