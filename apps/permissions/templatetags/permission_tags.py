from django import template
from apps.permissions.decorators import check_user_module_permission

register = template.Library()

@register.simple_tag(takes_context=True)
def has_permission(context, module_name, permission_type='view'):
    """
    Template tag to conditionally render UI elements based on module permissions.
    Usage: {% has_permission 'assets' 'create' as can_create_asset %}
    """
    request = context.get('request')
    if not request or not hasattr(request, 'user'):
        return False
    return check_user_module_permission(request.user, module_name, permission_type)

@register.filter
def in_role(user, role_list):
    """
    Check if user is in any of the comma-separated roles.
    Usage: {% if user|in_role:"super_admin,organization_admin" %}
    """
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or getattr(user, 'role', '') == 'super_admin':
        return True
    roles = [r.strip() for r in role_list.split(',')]
    return getattr(user, 'role', '') in roles
