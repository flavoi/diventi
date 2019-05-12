from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin

from diventi.core.admin import DiventiTranslationAdmin

from .models import DiventiUser, DiventiAvatar, DiventiProfilePic, DiventiCover, Achievement, Role


class DiventiUserAdmin(UserAdmin, DiventiTranslationAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nametag', 'first_name', 'language', 'has_agreed_gdpr', 'bio', 'avatar', 'cover', 'profilepic', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('nametag', 'first_name', 'last_name', 'language', 'bio', 'avatar', 'profilepic')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = auth_admin.UserChangeForm
    add_form = auth_admin.UserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_login', 'date_joined', 'language', 'has_agreed_gdpr', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    readonly_fields = ('nametag', 'last_login', 'date_joined',)


class DiventiAvatarAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag', 'staff_only')


class DiventiProfilePicAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag',)


class DiventiCoverAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag')


class DiventiUserInline(admin.TabularInline):
    model = Achievement.users.through


class AchievementAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'description')
    inlines = [
        DiventiUserInline,
    ]


class RoleAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'description')


admin.site.register(DiventiUser, DiventiUserAdmin)
admin.site.register(DiventiAvatar, DiventiAvatarAdmin)
admin.site.register(DiventiProfilePic, DiventiProfilePicAdmin)
admin.site.register(DiventiCover, DiventiCoverAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Role, RoleAdmin)