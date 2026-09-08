"""
InfraFlowX - Signal Receivers & Event Hooks for Contractors App
Automatically executes audit logging, cache invalidation, and workflow triggers.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger("infraflowx.contractors")


@receiver(post_save)
def handle_contractors_post_save(sender, instance, created, **kwargs):
    if sender.__module__.startswith("apps.contractors.models"):
        action = "CREATED" if created else "UPDATED"
        logger.info(f"[CONTRACTORS_SIGNAL] {sender.__name__} #{instance.pk} {action}")


@receiver(post_delete)
def handle_contractors_post_delete(sender, instance, **kwargs):
    if sender.__module__.startswith("apps.contractors.models"):
        logger.warning(f"[CONTRACTORS_SIGNAL] {sender.__name__} #{instance.pk} DELETED")
