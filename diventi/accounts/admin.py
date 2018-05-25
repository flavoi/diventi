from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from diventi.core.admin import DiventiTranslationAdmin

from .models import DiventiUser, DiventiAvatar, DiventiCover, Achievement
from .forms import DiventiUserUpdateForm, DiventiUserCreationForm


class DiventiUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'bio', 'avatar', 'language', 'cover', 'profilepic', 'role', 'has_agreed_gdpr')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_form = DiventiUserCreationForm
    form = DiventiUserUpdateForm
    model = DiventiUser
    list_display = ['username', 'language', 'is_active', 'is_staff', 'has_agreed_gdpr']


class DiventiAvatarAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag', 'staff_only')


class DiventiCoverAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag')


class DiventiUserInline(admin.TabularInline):
    model = Achievement.users.through

class AchievementAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'description')
    inlines = [
        DiventiUserInline,
    ]

admin.site.register(DiventiUser, DiventiUserAdmin)
admin.site.register(DiventiAvatar, DiventiAvatarAdmin)
admin.site.register(DiventiCover, DiventiCoverAdmin)
admin.site.register(Achievement, AchievementAdmin)