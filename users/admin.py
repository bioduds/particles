from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser', 'created_at')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Perfil', {'fields': ('role', 'bio', 'avatar')}),
    )
