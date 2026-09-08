"""
InfraFlowX - Signal Receivers & Event Hooks for Notifications App
Automatically executes audit logging, cache invalidation, and workflow triggers.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger("infraflowx.notifications")


@receiver(post_save)
def handle_notifications_post_save(sender, instance, created, **kwargs):
    if sender.__module__.startswith("apps.notifications.models"):
        action = "CREATED" if created else "UPDATED"
        logger.info(f"[NOTIFICATIONS_SIGNAL] {sender.__name__} #{instance.pk} {action}")


@receiver(post_delete)
def handle_notifications_post_delete(sender, instance, **kwargs):
    if sender.__module__.startswith("apps.notifications.models"):
        logger.warning(f"[NOTIFICATIONS_SIGNAL] {sender.__name__} #{instance.pk} DELETED")
