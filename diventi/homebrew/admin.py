from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from diventi.core.admin import DiventiTranslationAdmin

from .models import Brew


class BrewAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'description']
    readonly_fields = ['created', 'modified']
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Brew, BrewAdmin)
