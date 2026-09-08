import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset
from apps.projects.models import Project
from apps.workorders.models import WorkOrder
from apps.contractors.models import Contractor

class Expense(models.Model):
    """
    Line-item operational and capital expense tracking with multi-tier audit approvals.
    """
    CATEGORY_CHOICES = [
        ('LABOR', _('Field Engineering & Direct Labor')),
        ('MATERIALS', _('Paving / Structural Materials & Concrete')),
        ('EQUIPMENT', _('Heavy Machinery Rental & Fuel')),
        ('CONTRACTOR', _('Prime Contractor Progress Billing')),
        ('TRANSPORT', _('Logistics & Fleet Haulage')),
        ('EMERGENCY', _('Emergency Incident Response Action')),
        ('PERMITS', _('Environmental & Municipal Permits')),
        ('OTHER', _('Miscellaneous Expense')),
    ]

    APPROVAL_STATUS_CHOICES = [
        ('PENDING', _('Pending Management Review')),
        ('APPROVED', _('Approved by Finance Officer')),
        ('REJECTED', _('Rejected / Disputed')),
        ('REIMBURSED', _('Reimbursed / Settled')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('Expense Voucher Reference')
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        verbose_name=_('Target Asset')
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        verbose_name=_('Capital Project (Optional)')
    )
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        verbose_name=_('Work Order (Optional)')
    )
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses',
        verbose_name=_('Vendor / Payee')
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='MATERIALS',
        verbose_name=_('Expense Classification')
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_('Total Expense Amount ($)')
    )
    expense_date = models.DateField(
        verbose_name=_('Incurred Date')
    )
    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Vendor Invoice / Bill No.')
    )
    description = models.TextField(
        verbose_name=_('Expense Summary & Line-Item Justification')
    )
    receipt_file = models.FileField(
        upload_to='invoices/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Invoice / Receipt Document')
    )
    approval_status = models.CharField(
        max_length=50,
        choices=APPROVAL_STATUS_CHOICES,
        default='PENDING',
        db_index=True,
        verbose_name=_('Approval Status')
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_expenses',
        verbose_name=_('Approving Authority')
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Approval Timestamp'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-expense_date', '-created_at']
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses & Invoices')
        indexes = [
            models.Index(fields=['expense_id']),
            models.Index(fields=['approval_status', '-expense_date']),
        ]

    def __str__(self):
        return f"[{self.expense_id}] {self.get_category_display()} - ${self.amount} ({self.get_approval_status_display()})"
