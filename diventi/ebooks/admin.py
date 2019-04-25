from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from .models import Section


class SectionAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index']
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (_('Editing'), {
            'fields': ('title', 'order_index', 'slug'),
        }),
        (_('Content'), {
            'fields': ('content',),
        }),
    )
    ordering = ['order_index']

admin.site.register(Section, SectionAdmin)
