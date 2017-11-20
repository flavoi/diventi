from django.contrib import admin

from .models import Product, Event


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


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'featured']    
    inlines = [
        EventInline,
    ]
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_published, make_unpublished]


admin.site.register(Product, ProductAdmin)
