"""
InfraFlowX - Signal Receivers & Event Hooks for Schedules App
Automatically executes audit logging, cache invalidation, and workflow triggers.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger("infraflowx.schedules")


@receiver(post_save)
def handle_schedules_post_save(sender, instance, created, **kwargs):
    if sender.__module__.startswith("apps.schedules.models"):
        action = "CREATED" if created else "UPDATED"
        logger.info(f"[SCHEDULES_SIGNAL] {sender.__name__} #{instance.pk} {action}")


@receiver(post_delete)
def handle_schedules_post_delete(sender, instance, **kwargs):
    if sender.__module__.startswith("apps.schedules.models"):
        logger.warning(f"[SCHEDULES_SIGNAL] {sender.__name__} #{instance.pk} DELETED")
