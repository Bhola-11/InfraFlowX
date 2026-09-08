from django.conf import settings
from .models import SYSTEM_MODULES

def enterprise_context(request):
    """
    Global enterprise context processor exposing user role flags, system modules, and active environment metadata.
    """
    user = getattr(request, 'user', None)
    is_auth = user and user.is_authenticated

    context = {
        'APP_NAME': 'InfraFlowX',
        'APP_VERSION': 'v2.4 Enterprise',
        'APP_TAGLINE': 'Enterprise Infrastructure & Asset Lifecycle Management Platform',
        'SYSTEM_MODULES': SYSTEM_MODULES,
        'IS_SUPERUSER': is_auth and (user.is_superuser or getattr(user, 'role', '') == 'super_admin'),
        'IS_ORG_ADMIN': is_auth and getattr(user, 'role', '') in ['super_admin', 'organization_admin'],
        'IS_MANAGER': is_auth and getattr(user, 'role', '') in [
            'super_admin', 'organization_admin', 'infrastructure_manager', 
            'asset_manager', 'project_manager', 'maintenance_manager', 'contractor_manager', 'finance_manager'
        ],
        'IS_INSPECTOR': is_auth and getattr(user, 'role', '') in ['inspector', 'field_engineer', 'infrastructure_manager', 'asset_manager'],
        'USER_ROLE': getattr(user, 'role', '') if is_auth else None,
        'USER_ROLE_DISPLAY': user.get_role_display() if is_auth and hasattr(user, 'get_role_display') else '',
    }
    return context
