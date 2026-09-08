from apps.permissions.models import RolePermission


class PermissionService:
    @staticmethod
    def user_has_permission(user, module, action='view'):
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        perm = RolePermission.objects.filter(role=user.role, module=module).first()
        if not perm:
            return False
        field_name = f"can_{action.lower()}"
        return getattr(perm, field_name, False)
