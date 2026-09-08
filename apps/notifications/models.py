from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    """
    Enterprise In-App Notification and Alert system.
    """
    TYPE_CHOICES = [
        ('MAINTENANCE', _('Maintenance Reminder')),
        ('WORKORDER', _('Work Order Notification')),
        ('INSPECTION', _('Inspection Alert')),
        ('INCIDENT', _('Emergency Incident Alert')),
        ('BUDGET', _('Budget Limit Threshold Alert')),
        ('INVENTORY', _('Low Stock Warning')),
        ('PROJECT', _('Project Deadline Milestone')),
        ('SUPPORT', _('Support Ticket Update')),
        ('SYSTEM', _('System Alert')),
    ]

    PRIORITY_CHOICES = [
        ('LOW', _('Low')),
        ('MEDIUM', _('Medium')),
        ('HIGH', _('High')),
        ('CRITICAL', _('Critical / Urgent')),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Recipient User')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name=_('Sender User (Optional)')
    )
    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='SYSTEM',
        verbose_name=_('Notification Type')
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name=_('Priority')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Alert Title')
    )
    message = models.TextField(
        verbose_name=_('Notification Body')
    )
    link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Target Action URL')
    )
    is_read = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_('Is Read')
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Read Timestamp')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Created At')
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title} -> {self.recipient.username}"
