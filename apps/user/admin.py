from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminConfig(UserAdmin):
    ordering = ('-email',)
    list_display = ('email', 'user_name', 'name', 'phone_number', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'name', 'phone_number', 'last_login')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )


admin.site.register(User, UserAdminConfig)