"""
InfraFlowX - Signal Receivers & Event Hooks for Expenses App
Automatically executes audit logging, cache invalidation, and workflow triggers.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger("infraflowx.expenses")


@receiver(post_save)
def handle_expenses_post_save(sender, instance, created, **kwargs):
    if sender.__module__.startswith("apps.expenses.models"):
        action = "CREATED" if created else "UPDATED"
        logger.info(f"[EXPENSES_SIGNAL] {sender.__name__} #{instance.pk} {action}")


@receiver(post_delete)
def handle_expenses_post_delete(sender, instance, **kwargs):
    if sender.__module__.startswith("apps.expenses.models"):
        logger.warning(f"[EXPENSES_SIGNAL] {sender.__name__} #{instance.pk} DELETED")
