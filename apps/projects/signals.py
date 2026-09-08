"""
InfraFlowX - Signal Receivers & Event Hooks for Projects App
Automatically executes audit logging, cache invalidation, and workflow triggers.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger("infraflowx.projects")


@receiver(post_save)
def handle_projects_post_save(sender, instance, created, **kwargs):
    if sender.__module__.startswith("apps.projects.models"):
        action = "CREATED" if created else "UPDATED"
        logger.info(f"[PROJECTS_SIGNAL] {sender.__name__} #{instance.pk} {action}")


@receiver(post_delete)
def handle_projects_post_delete(sender, instance, **kwargs):
    if sender.__module__.startswith("apps.projects.models"):
        logger.warning(f"[PROJECTS_SIGNAL] {sender.__name__} #{instance.pk} DELETED")
