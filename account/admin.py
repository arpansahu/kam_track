from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'name', 'role', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'role')
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'password', 'role', 'profile_photo', 'country_code', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2', 'role', 'is_staff', 'is_active', 'profile_photo', 'country_code', 'phone_number'),
        }),
    )

    # Removed `filter_horizontal` since `groups` and `user_permissions` don't exist
    filter_horizontal = ()

admin.site.register(Account, AccountAdmin)
