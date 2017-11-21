from django.contrib import admin

from .models import Product, Event, Chapter, Characteristic, ImagePreview


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Mark selected products as published"


def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = "Mark selected products as hidden"


class EventInline(admin.TabularInline):
    model = Event
    fields = ('title', 'icon', 'color', 'description', 'event_date')
    extra = 0

class ChapterInline(admin.TabularInline):
    model = Chapter
    fields = ('title', 'description')
    extra = 0

class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    fields = ('title', 'description')
    extra = 0


class ImagePreviewInline(admin.StackedInline):
    model = ImagePreview
    fields = ( 'label', 'image')
    extra = 0


class ImagePreviewAdmin(admin.ModelAdmin):
    list_display = ('label', 'image_tag')


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'featured']    
    inlines = [
        EventInline,
        ChapterInline,
        CharacteristicInline,
        ImagePreviewInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_published, make_unpublished]


admin.site.register(Product, ProductAdmin)
admin.site.register(ImagePreview, ImagePreviewAdmin)
