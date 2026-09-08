import threading

_local_storage = threading.local()

def get_current_request():
    """Retrieve the current thread request object."""
    return getattr(_local_storage, 'request', None)

def get_current_user():
    """Retrieve current thread user."""
    request = get_current_request()
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    return None

class AuditLoggingMiddleware:
    """
    Middleware that captures request information (IP, User, Agent) in thread-local storage for audit records.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local_storage.request = request
        
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        request.client_ip = ip
        request.user_agent_str = request.META.get('HTTP_USER_AGENT', '')[:255]

        response = self.get_response(request)
        return response
