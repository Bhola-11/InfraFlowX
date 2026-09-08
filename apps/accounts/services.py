"""
Accounts & Authentication Services
"""
from apps.accounts.models import User
from apps.audit.utils import log_audit_event


class AccountService:
    @staticmethod
    def deactivate_user(user_id, admin_user=None):
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save(update_fields=['is_active'])
        
        log_audit_event(
            action='UPDATE',
            module='accounts',
            object_id=str(user.id),
            object_repr=user.username,
            description=f"User {user.username} deactivated by administrator",
            user=admin_user
        )
        return user
