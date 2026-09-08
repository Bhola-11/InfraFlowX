"""
InfraFlowX - Signal Receivers & Event Hooks for Assets App
Automatically executes audit logging, cache invalidation, and workflow triggers.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger("infraflowx.assets")


@receiver(post_save)
def handle_assets_post_save(sender, instance, created, **kwargs):
    if sender.__module__.startswith("apps.assets.models"):
        action = "CREATED" if created else "UPDATED"
        logger.info(f"[ASSETS_SIGNAL] {sender.__name__} #{instance.pk} {action}")


@receiver(post_delete)
def handle_assets_post_delete(sender, instance, **kwargs):
    if sender.__module__.startswith("apps.assets.models"):
        logger.warning(f"[ASSETS_SIGNAL] {sender.__name__} #{instance.pk} DELETED")
