from django.contrib import admin
from .models import RolePermission, UserPermissionOverride

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module', 'can_view', 'can_create', 'can_edit', 'can_delete', 'can_approve', 'can_export')
    list_filter = ('role', 'module')
    search_fields = ('role', 'module')

@admin.register(UserPermissionOverride)
class UserPermissionOverrideAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'can_view', 'can_create', 'can_edit', 'can_delete', 'can_approve', 'can_export')
    list_filter = ('module', 'user')
    search_fields = ('user__username', 'module')
