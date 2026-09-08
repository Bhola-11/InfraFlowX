from django.utils import timezone
from .models import Notification

def send_notification(recipient, title, message, notification_type='SYSTEM', priority='MEDIUM', link=None, sender=None):
    """
    Helper function to dispatch in-app notifications.
    """
    if recipient is None:
        return None
    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        priority=priority,
        title=title,
        message=message,
        link=link
    )

def broadcast_notification_to_role(role_name, title, message, notification_type='SYSTEM', priority='MEDIUM', link=None):
    """
    Broadcasts notification to all users matching a specified enterprise role.
    """
    from apps.accounts.models import User
    users = User.objects.filter(role=role_name, is_active=True)
    created_list = []
    for user in users:
        created_list.append(
            Notification(
                recipient=user,
                notification_type=notification_type,
                priority=priority,
                title=title,
                message=message,
                link=link
            )
        )
    if created_list:
        return Notification.objects.bulk_create(created_list)
    return []
