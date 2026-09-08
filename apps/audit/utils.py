from .models import AuditLog
from .middleware import get_current_request

def log_audit_event(action, module, object_id=None, object_repr=None, changes=None, description="", user=None, request=None):
    """
    Central utility function to log any enterprise audit event.
    """
    if request is None:
        request = get_current_request()

    ip_address = None
    user_agent = ""

    if request:
        if user is None and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        ip_address = getattr(request, 'client_ip', None)
        user_agent = getattr(request, 'user_agent_str', '')

    return AuditLog.objects.create(
        user=user,
        action=action,
        module=module,
        object_id=str(object_id) if object_id is not None else None,
        object_repr=str(object_repr)[:255] if object_repr is not None else None,
        changes=changes or {},
        description=description,
        ip_address=ip_address,
        user_agent=user_agent
    )
