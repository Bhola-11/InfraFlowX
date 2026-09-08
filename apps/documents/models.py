import uuid
from django.db import models
from django.conf import settings
from apps.organizations.models import Organization
from apps.assets.models import Asset
from apps.projects.models import Project


class DocumentCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Document Category'
        verbose_name_plural = 'Document Categories'

    def __str__(self):
        return self.name


class Document(models.Model):
    CONFIDENTIALITY_LEVELS = [
        ('PUBLIC', 'Public / Unclassified'),
        ('INTERNAL', 'Internal Use Only'),
        ('RESTRICTED', 'Restricted'),
        ('CONFIDENTIAL', 'Strictly Confidential'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved / Effective'),
        ('ARCHIVED', 'Archived / Superseded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doc_number = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/%Y/%m/', blank=True, null=True)
    file_size_bytes = models.BigIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    current_version = models.CharField(max_length=20, default='1.0')
    is_blueprint = models.BooleanField(default=False, help_text="Is an engineering CAD blueprint / structural schematic")
    confidentiality = models.CharField(max_length=30, choices=CONFIDENTIALITY_LEVELS, default='INTERNAL')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='APPROVED')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_documents')
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.doc_number} - {self.title} (v{self.current_version})"

    @property
    def file_size_display(self):
        if not self.file_size_bytes:
            return "0 KB"
        kb = self.file_size_bytes / 1024
        if kb < 1024:
            return f"{kb:.1f} KB"
        return f"{kb / 1024:.2f} MB"


class DocumentVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=20)
    file = models.FileField(upload_to='document_versions/%Y/%m/', blank=True, null=True)
    change_log = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ('document', 'version_number')
        verbose_name = 'Document Version'
        verbose_name_plural = 'Document Versions'

    def __str__(self):
        return f"{self.document.doc_number} v{self.version_number}"


class BlueprintMetadata(models.Model):
    SHEET_SIZES = [
        ('A0', 'A0 (841 x 1189 mm)'),
        ('A1', 'A1 (594 x 841 mm)'),
        ('A2', 'A2 (420 x 594 mm)'),
        ('A3', 'A3 (297 x 420 mm)'),
        ('A4', 'A4 (210 x 297 mm)'),
        ('CUSTOM', 'Custom Dimensions'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='blueprint_info')
    drawing_number = models.CharField(max_length=100)
    scale_ratio = models.CharField(max_length=50, default='1:100')
    sheet_size = models.CharField(max_length=20, choices=SHEET_SIZES, default='A1')
    cad_software = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. AutoCAD, Revit, MicroStation")
    engineer_signoff_name = models.CharField(max_length=150, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Blueprint Metadata'
        verbose_name_plural = 'Blueprint Metadata'

    def __str__(self):
        return f"Drawing {self.drawing_number} for {self.document.title}"
