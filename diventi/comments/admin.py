from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import DiventiComment

admin.site.register(DiventiComment, MPTTModelAdmin)
