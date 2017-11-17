from django.contrib import admin

from .models import Article, Category, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ('title', 'file')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'hot']
    readonly_fields = ['created', 'modified']
    prepopulated_fields = {"slug": ("title",)}   

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)