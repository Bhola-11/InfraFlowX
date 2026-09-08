from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

SYSTEM_MODULES = [
    ('accounts', _('Accounts & Users')),
    ('organizations', _('Organizations & Hierarchy')),
    ('employees', _('Employees & Staff')),
    ('assets', _('Central Asset Registry')),
    ('roads', _('Road Infrastructure')),
    ('bridges', _('Bridge Infrastructure')),
    ('buildings', _('Building Infrastructure')),
    ('facilities', _('Facilities & MEP')),
    ('locations', _('Geospatial Locations & GIS')),
    ('inspections', _('Inspection Operations')),
    ('conditions', _('Condition Scoring & Curves')),
    ('maintenance', _('Maintenance Schedules & Plans')),
    ('workorders', _('Work Orders & Execution')),
    ('projects', _('Capital Projects & Gantt')),
    ('contractors', _('Contractors & Vendors')),
    ('budgets', _('Budgets & Fiscal Allocations')),
    ('expenses', _('Expense Tracking & Approvals')),
    ('incidents', _('Incident Management & Safety')),
    ('documents', _('Document Management System')),
    ('inventory', _('Maintenance Inventory & Spare Parts')),
    ('schedules', _('Recurring Scheduler')),
    ('notifications', _('Notification Hub')),
    ('analytics', _('Enterprise Analytics & KPIs')),
    ('reports', _('Reports & Data Exports')),
    ('support', _('Support Helpdesk & Complaints')),
    ('permissions', _('Security & Role Permissions')),
    ('audit', _('Audit Logs & Compliance')),
]

class RolePermission(models.Model):
    """
    Granular permission rule per role and module.
    """
    role = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name=_('Role Key')
    )
    module = models.CharField(
        max_length=50,
        choices=SYSTEM_MODULES,
        db_index=True,
        verbose_name=_('Module Name')
    )
    can_view = models.BooleanField(default=True, verbose_name=_('Can View'))
    can_create = models.BooleanField(default=False, verbose_name=_('Can Create'))
    can_edit = models.BooleanField(default=False, verbose_name=_('Can Edit'))
    can_delete = models.BooleanField(default=False, verbose_name=_('Can Delete'))
    can_approve = models.BooleanField(default=False, verbose_name=_('Can Approve'))
    can_export = models.BooleanField(default=False, verbose_name=_('Can Export Data'))

    class Meta:
        verbose_name = _('Role Permission Matrix Entry')
        verbose_name_plural = _('Role Permission Matrix')
        unique_together = ('role', 'module')
        ordering = ['role', 'module']

    def __str__(self):
        return f"[{self.role}] - {self.get_module_display()} (V:{self.can_view}, C:{self.can_create}, E:{self.can_edit}, D:{self.can_delete}, A:{self.can_approve})"


class UserPermissionOverride(models.Model):
    """
    Per-user override on top of default role permissions.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='permission_overrides',
        verbose_name=_('Target User')
    )
    module = models.CharField(
        max_length=50,
        choices=SYSTEM_MODULES,
        verbose_name=_('Module Name')
    )
    can_view = models.BooleanField(default=True)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    can_export = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('User Permission Override')
        verbose_name_plural = _('User Permission Overrides')
        unique_together = ('user', 'module')

    def __str__(self):
        return f"Override: {self.user.username} - {self.get_module_display()}"
