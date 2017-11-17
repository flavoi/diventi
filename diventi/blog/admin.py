from django.contrib import admin

from .models import Article, Category, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ('title', 'file')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'hot', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)}   

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)