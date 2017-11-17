from django.contrib import admin

from .models import Article, Category, Attachment


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Mark selected stories as published"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'hot', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}   
    actions = [make_published]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)