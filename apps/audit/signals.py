"""
InfraFlowX - Signal Receivers & Event Hooks for Audit App
Automatically executes audit logging, cache invalidation, and workflow triggers.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger("infraflowx.audit")


@receiver(post_save)
def handle_audit_post_save(sender, instance, created, **kwargs):
    if sender.__module__.startswith("apps.audit.models"):
        action = "CREATED" if created else "UPDATED"
        logger.info(f"[AUDIT_SIGNAL] {sender.__name__} #{instance.pk} {action}")


@receiver(post_delete)
def handle_audit_post_delete(sender, instance, **kwargs):
    if sender.__module__.startswith("apps.audit.models"):
        logger.warning(f"[AUDIT_SIGNAL] {sender.__name__} #{instance.pk} DELETED")
