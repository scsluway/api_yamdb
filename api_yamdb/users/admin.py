from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'is_staff', 'role', 'confirmation_code'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    list_editable = ['role']


admin.site.register(User, CustomUserAdmin)
