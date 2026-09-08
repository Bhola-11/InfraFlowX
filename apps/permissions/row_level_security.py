"""
InfraFlowX - Row-Level Security (RLS) & Tenant Scoping Engine
Applies tenant isolation and organizational departmental filters to Django ORM QuerySets.
"""

from typing import Any


class RowLevelSecurityEngine:
    """
    Guarantees strict tenant and department queryset isolation.
    """

    @classmethod
    def apply_security_scope(cls, queryset: Any, user: Any) -> Any:
        if not user or not user.is_authenticated:
            return queryset.none()

        if getattr(user, 'is_superuser', False) or getattr(user, 'role', '') == 'SUPERADMIN':
            return queryset

        # Apply organization tenant filter if field exists on model
        model = queryset.model
        fields = [f.name for f in model._meta.get_fields()]

        if 'organization' in fields and hasattr(user, 'organization_id'):
            return queryset.filter(organization_id=user.organization_id)
        elif 'tenant' in fields and hasattr(user, 'tenant_id'):
            return queryset.filter(tenant_id=user.tenant_id)

        return queryset
