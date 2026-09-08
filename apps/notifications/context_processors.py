from .models import Notification

def unread_notifications_context(request):
    """
    Supplies unread notification count and latest 5 unread alerts to all views.
    """
    if request.user.is_authenticated:
        unread_qs = Notification.objects.filter(recipient=request.user, is_read=False)
        unread_count = unread_qs.count()
        recent_notifications = unread_qs[:5]
        return {
            'unread_notifications_count': unread_count,
            'recent_notifications': recent_notifications,
        }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }
