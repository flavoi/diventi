from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from .models import Section


class SectionAdmin(DiventiTranslationAdmin):
    model = Section
    list_display = ['title', 'order_index']
    fieldsets = (
        (_('Editing'), {
            'fields': ('title', 'order_index',),
        }),
        (_('Content'), {
            'fields': ('content',),
        }),
    )

admin.site.register(Section, SectionAdmin)
