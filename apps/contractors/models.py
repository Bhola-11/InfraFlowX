import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.organizations.models import Organization

class Contractor(models.Model):
    """
    Contractor vendor registry for infrastructure construction, maintenance and emergency repairs.
    """
    SPECIALIZATION_CHOICES = [
        ('ASPHALT_PAVING', _('Highway Milling & Asphalt Paving')),
        ('BRIDGE_STRUCTURAL', _('Structural Steel & Bridge Rehabilitation')),
        ('MEP_HVAC', _('Mechanical, Electrical & HVAC Plant')),
        ('ELECTRICAL_GRID', _('High Voltage & Grid Utilities')),
        ('PLUMBING_WATER', _('Municipal Water Main & Storm Drainage')),
        ('TUNNEL_EARTHWORK', _('Excavation, Tunnels & Geotechnical')),
        ('GENERAL_CONSTRUCTION', _('General Civil Construction')),
        ('SECURITY_FIRE', _('Fire Suppression & Life Safety Systems')),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', _('Active / Approved Vendor')),
        ('PROBATION', _('Probationary / Monitoring')),
        ('SUSPENDED', _('Suspended / Compliance Hold')),
        ('BLACKLISTED', _('Blacklisted / Disqualified')),
        ('INACTIVE', _('Inactive / Expired Agreement')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='contractors',
        verbose_name=_('Primary Authorizing Agency')
    )
    company_name = models.CharField(max_length=255, unique=True, verbose_name=_('Contractor Company Legal Name'))
    registration_number = models.CharField(max_length=100, unique=True, verbose_name=_('Business License / Vendor ID'))
    contact_person = models.CharField(max_length=150, verbose_name=_('Key Account Manager / Contact'))
    email = models.EmailField(verbose_name=_('Business Email'))
    phone = models.CharField(max_length=50, verbose_name=_('Contact Phone'))
    address = models.TextField(verbose_name=_('Head Office Address'))
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, default='GENERAL_CONSTRUCTION')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.50, verbose_name=_('SLA Performance Rating (1.00-5.00)'))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='ACTIVE', db_index=True)
    contract_start = models.DateField(null=True, blank=True, verbose_name=_('Master Agreement Start Date'))
    contract_end = models.DateField(null=True, blank=True, verbose_name=_('Master Agreement Expiry Date'))
    insurance_policy_number = models.CharField(max_length=100, blank=True, verbose_name=_('Commercial Liability Policy'))
    insurance_expiry = models.DateField(null=True, blank=True, verbose_name=_('Insurance Expiration Date'))
    notes = models.TextField(blank=True, verbose_name=_('Vendor Qualifications & Notes'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']
        verbose_name = _('Contractor')
        verbose_name_plural = _('Contractors')

    def __str__(self):
        return f"{self.company_name} ({self.get_specialization_display()}) - {self.get_status_display()}"


class ContractAgreement(models.Model):
    """
    Formal procurement contract agreement signed with a contractor.
    """
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='agreements')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='procurement_contracts')
    contract_title = models.CharField(max_length=255, verbose_name=_('Contract Title'))
    contract_number = models.CharField(max_length=100, unique=True, verbose_name=_('Contract Reference Number'))
    total_contract_value = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name=_('Total Value ($)'))
    start_date = models.DateField()
    end_date = models.DateField()
    scope_summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    document_file = models.FileField(upload_to='contracts/%Y/%m/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = _('Contract Agreement')
        verbose_name_plural = _('Contract Agreements')

    def __str__(self):
        return f"[{self.contract_number}] {self.contract_title} - ${self.total_contract_value}"


class ContractorEvaluation(models.Model):
    """
    Periodic SLA performance evaluation scorecard.
    """
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='evaluations')
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    evaluation_date = models.DateField(auto_now_add=True)
    quality_score = models.IntegerField(default=4, verbose_name=_('Work Quality (1-5)'))
    safety_score = models.IntegerField(default=5, verbose_name=_('Safety & Compliance (1-5)'))
    timeliness_score = models.IntegerField(default=4, verbose_name=_('Timeliness & Milestones (1-5)'))
    overall_score = models.DecimalField(max_digits=3, decimal_places=2, default=4.33)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-evaluation_date']
        verbose_name = _('Contractor Evaluation')
        verbose_name_plural = _('Contractor Evaluations')

    def __str__(self):
        return f"{self.contractor.company_name} - Evaluation: {self.overall_score}/5.00"
