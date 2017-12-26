from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import DiventiUser, DiventiAvatar, DiventiCover


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'bio', 'avatar', 'cover', 'profilepic', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio', 'avatar', 'profilepic')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)

class DiventiAvatarAdmin(admin.ModelAdmin):
    list_display= ( 'label', 'image_tag', 'staff_only')

class DiventiCoverAdmin(admin.ModelAdmin):
    list_display= ( 'label', 'image_tag')

admin.site.register(DiventiUser, UserAdmin)
admin.site.register(DiventiAvatar, DiventiAvatarAdmin)
admin.site.register(DiventiCover, DiventiCoverAdmin)