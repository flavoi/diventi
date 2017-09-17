from django.contrib import admin

from .models import Post, Category, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ('title', 'file')


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'hot']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        AttachmentInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)