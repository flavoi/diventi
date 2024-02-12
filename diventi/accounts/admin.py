from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin

from diventi.core.admin import DiventiTranslationAdmin

from .models import (
    DiventiUser, 
    DiventiAvatar, 
    DiventiProfilePic, 
    DiventiCover,
    Role,
    Award,
)


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
    ordering = ('-date_joined',)
    readonly_fields = ('nametag', 'last_login', 'date_joined',)


class DiventiAvatarAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag', 'staff_only')


class DiventiProfilePicAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag',)


class DiventiCoverAdmin(DiventiTranslationAdmin):
    list_display = ('label', 'image_tag')


class RoleAdmin(DiventiTranslationAdmin):
    list_display = ('title', 'description')


class AwardAdmin(admin.ModelAdmin):
    list_display = ('pk', 'awarded_user', 'deed', 'notified', 'created')
    readonly_fields = ['created',]
    search_fields = ['awarded_user__first_name']
    list_filter = ['deed',]


admin.site.register(DiventiUser, DiventiUserAdmin)
admin.site.register(DiventiAvatar, DiventiAvatarAdmin)
admin.site.register(DiventiProfilePic, DiventiProfilePicAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Award, AwardAdmin)

