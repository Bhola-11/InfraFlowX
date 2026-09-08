from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserLoginSession

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Settings'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'organization', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'organization')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'badge_number')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'job_title', 'badge_number', 'avatar')}),
        ('Enterprise Roles & Org', {'fields': ('role', 'organization', 'is_two_factor_enabled')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'last_activity', 'date_joined')}),
        ('Administrative Notes', {'fields': ('notes',)}),
    )

@admin.register(UserLoginSession)
class UserLoginSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time', 'logout_time', 'is_active')
    list_filter = ('is_active', 'login_time')
    search_fields = ('user__username', 'ip_address')
