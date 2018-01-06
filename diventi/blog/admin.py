from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from .models import Article, Category


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = _("Mark selected stories as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = _("Mark selected stories as hidden")


class ArticleAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'category', 'hot', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    actions = [make_published, make_unpublished]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)