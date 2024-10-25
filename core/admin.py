from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'last_login',
        'Name',
        'Image',
        'Username',
        'Phone',
        'Group',
        'Address',
        'AutoShow',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'last_login',
        'AutoShow',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    raw_id_fields = ('groups', 'user_permissions')