from django.contrib import admin

from .models import Article, Category, HeaderImage, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ('title', 'file')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'hot']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        AttachmentInline,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(HeaderImage)