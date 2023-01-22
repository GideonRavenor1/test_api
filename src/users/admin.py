from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAppAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'role')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'email',
                    'password',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                    'is_staff',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            },
        ),
        (
            _('Additional information'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'role',
                )
            },
        ),
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    list_filter = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'role')
    list_editable = ('is_superuser', 'role')
    list_display_links = ('username',)
