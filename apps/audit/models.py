from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class AuditLog(models.Model):
    """
    Comprehensive Audit Trail Log storing all user and system actions with detailed delta changes.
    """
    ACTION_CHOICES = [
        ('LOGIN', _('User Login')),
        ('LOGOUT', _('User Logout')),
        ('CREATE', _('Record Created')),
        ('UPDATE', _('Record Updated')),
        ('DELETE', _('Record Deleted')),
        ('ASSET_CHANGE', _('Asset State Changed')),
        ('MAINTENANCE_ACTION', _('Maintenance Executed')),
        ('PROJECT_CHANGE', _('Project Progress Updated')),
        ('BUDGET_ACTION', _('Budget Allocation/Expense')),
        ('PERMISSION_CHANGE', _('Permissions Modified')),
        ('DOCUMENT_ACTION', _('Document Upload/Download/Delete')),
        ('EXPORT', _('Data Exported')),
        ('SYSTEM', _('System Event')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name=_('Actor / User')
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        default='SYSTEM',
        db_index=True,
        verbose_name=_('Action Performed')
    )
    module = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_('System Module / App')
    )
    object_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('Target Object ID')
    )
    object_repr = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Target Object Display')
    )
    changes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Field Changes (Diff)')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Action Description')
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP Address')
    )
    user_agent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('User Agent Browser')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Timestamp')
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['module', '-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]

    def __str__(self):
        user_display = self.user.get_full_name() if self.user else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {user_display} - {self.get_action_display()} on {self.module}"
