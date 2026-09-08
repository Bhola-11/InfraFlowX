import uuid
from django.db import models
from django.conf import settings


class ReportTemplate(models.Model):
    MODULE_CHOICES = [
        ('ASSETS', 'Asset Registry & Valuation'),
        ('WORKORDERS', 'Work Order Performance & Backlog'),
        ('INSPECTIONS', 'Condition & Inspection Audits'),
        ('FINANCIALS', 'Budget vs Actual Expenses'),
        ('CONTRACTORS', 'Contractor Performance & SLA'),
        ('INCIDENTS', 'Emergency Incidents & Response Logs'),
        ('INVENTORY', 'Stock Valuation & Consumption'),
    ]

    FORMAT_CHOICES = [
        ('CSV', 'Comma-Separated Values (CSV)'),
        ('EXCEL', 'Microsoft Excel (XLSX)'),
        ('JSON', 'JSON Data Export'),
        ('PDF', 'PDF Document'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=60, unique=True)
    module = models.CharField(max_length=30, choices=MODULE_CHOICES)
    default_format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='CSV')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['module', 'title']
        verbose_name = 'Report Template'
        verbose_name_plural = 'Report Templates'

    def __str__(self):
        return f"[{self.get_module_display()}] {self.title}"


class GeneratedReport(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Generation'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='generated_reports')
    report_name = models.CharField(max_length=255)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    file_format = models.CharField(max_length=20, choices=ReportTemplate.FORMAT_CHOICES, default='CSV')
    file = models.FileField(upload_to='reports/%Y/%m/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    row_count = models.PositiveIntegerField(default=0)
    file_size_kb = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    execution_time_sec = models.DecimalField(max_digits=6, decimal_places=3, default=0.000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Generated Report'
        verbose_name_plural = 'Generated Reports'

    def __str__(self):
        return f"{self.report_name} ({self.get_file_format_display()}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
