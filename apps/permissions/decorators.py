from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from .models import RolePermission, UserPermissionOverride

def check_user_module_permission(user, module_name, permission_type='view'):
    """
    Evaluates whether user has the requested permission type on module.
    Superusers automatically have all permissions.
    """
    if not user.is_authenticated:
        return False

    if user.is_superuser or user.role == 'super_admin':
        return True

    # Check User override first
    override = UserPermissionOverride.objects.filter(user=user, module=module_name).first()
    if override:
        return getattr(override, f'can_{permission_type}', False)

    # Check Role-based permissions
    role_perm = RolePermission.objects.filter(role=user.role, module=module_name).first()
    if role_perm:
        return getattr(role_perm, f'can_{permission_type}', False)

    # Organization Admin default fallback
    if user.role == 'organization_admin':
        return True

    # By default, viewers have read/view access to most modules
    if user.role == 'viewer' and permission_type in ['view', 'export']:
        return True

    return False


def permission_required(module_name, permission_type='view'):
    """
    Decorator for views checking module-level permission.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if not check_user_module_permission(request.user, module_name, permission_type):
                messages.error(request, f"Access Denied: You do not have '{permission_type}' permission for the {module_name} module.")
                raise PermissionDenied(f"Access Denied: You do not have '{permission_type}' permission for the {module_name} module.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def role_required(allowed_roles):
    """
    Decorator ensuring current user possesses one of the allowed roles.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or request.user.role == 'super_admin' or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, f"Access Denied: Your role ({request.user.get_role_display()}) cannot access this section.")
            raise PermissionDenied(f"Access Denied: Your role ({request.user.get_role_display()}) cannot access this section.")
        return _wrapped_view
    return decorator
