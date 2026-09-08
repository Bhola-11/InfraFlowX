import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.organizations.models import Organization, Department

class Budget(models.Model):
    """
    Fiscal budget allocation for capital works, operational maintenance, and departments.
    """
    BUDGET_TYPES = [
        ('ANNUAL_MASTER', _('Annual Master Operating Budget')),
        ('CAPITAL_PROJECT', _('Capital Infrastructure Project Fund')),
        ('MAINTENANCE_OPEX', _('Preventive & Corrective Maintenance OpEx')),
        ('DEPARTMENTAL', _('Departmental Operational Allocation')),
        ('EMERGENCY_RESERVE', _('Emergency Hazard Relief Fund')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_('Budget Code / Ledger ID')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Budget Program Title')
    )
    budget_type = models.CharField(
        max_length=50,
        choices=BUDGET_TYPES,
        default='MAINTENANCE_OPEX',
        verbose_name=_('Budget Classification')
    )
    fiscal_year = models.IntegerField(
        default=2026,
        verbose_name=_('Fiscal Year (FY)')
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='budgets',
        verbose_name=_('Owner Agency')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budgets',
        verbose_name=_('Assigned Department')
    )
    allocated_amount = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Total Allocated Amount ($)')
    )
    spent_amount = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Total Incurred Expenditures ($)')
    )
    notes = models.TextField(blank=True, verbose_name=_('Fiscal Notes & Authorization Mandate'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fiscal_year', 'title']
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets & Fiscal Allocations')

    def __str__(self):
        return f"[{self.fiscal_year}] {self.budget_code} - {self.title} (${self.allocated_amount})"

    @property
    def remaining_amount(self):
        return max(Decimal('0.00'), self.allocated_amount - self.spent_amount)

    @property
    def utilization_percentage(self):
        if self.allocated_amount > 0:
            return round((self.spent_amount / self.allocated_amount) * 100, 1)
        return 0.0


class BudgetAllocation(models.Model):
    """
    Line-item fiscal breakdown under a budget envelope.
    """
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='allocations')
    category_name = models.CharField(max_length=150, verbose_name=_('Allocation Line / Category'))
    allocated_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    spent_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['category_name']
        verbose_name = _('Budget Allocation Line')
        verbose_name_plural = _('Budget Allocation Lines')

    def __str__(self):
        return f"{self.budget.budget_code}: {self.category_name} (${self.allocated_amount})"
