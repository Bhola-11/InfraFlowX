import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Organization(models.Model):
    """
    Top-level enterprise entity / municipal department / infrastructure authority.
    """
    ORG_TYPES = [
        ('MUNICIPAL', _('Municipal Corporation')),
        ('HIGHWAY_AUTH', _('National / State Highway Authority')),
        ('PUBLIC_WORKS', _('Public Works Department (PWD)')),
        ('TRANSPORT', _('Transit & Transport Authority')),
        ('UTILITY', _('Water & Energy Utilities Authority')),
        ('PRIVATE_CONCESSIONAIRE', _('Private Infrastructure Concessionaire')),
        ('PORT_AIRPORT', _('Port & Aviation Authority')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Organization Name'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Org Short Code'))
    org_type = models.CharField(max_length=50, choices=ORG_TYPES, default='PUBLIC_WORKS', verbose_name=_('Organization Type'))
    tax_id = models.CharField(max_length=100, blank=True, verbose_name=_('Tax / Registration ID'))
    email = models.EmailField(blank=True, verbose_name=_('Official Email'))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_('Helpline / Phone'))
    website = models.URLField(blank=True, verbose_name=_('Official Website'))
    address = models.TextField(blank=True, verbose_name=_('Headquarters Address'))
    logo = models.ImageField(upload_to='org_logos/', null=True, blank=True, verbose_name=_('Organization Logo'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active Status'))
    annual_budget = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, verbose_name=_('Total Annual Budget ($)'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    def __str__(self):
        return f"{self.name} ({self.code})"


class Region(models.Model):
    """
    Geographic or administrative region under an organization.
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='regions',
        verbose_name=_('Organization')
    )
    name = models.CharField(max_length=200, verbose_name=_('Region Name'))
    code = models.CharField(max_length=50, verbose_name=_('Region Code'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    regional_head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_regions',
        verbose_name=_('Regional Director / Head')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    def __str__(self):
        return f"{self.name} - {self.organization.code}"


class Zone(models.Model):
    """
    Sub-regional operational zone.
    """
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='zones',
        verbose_name=_('Parent Region')
    )
    name = models.CharField(max_length=200, verbose_name=_('Zone Name'))
    code = models.CharField(max_length=50, verbose_name=_('Zone Code'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('region', 'code')
        ordering = ['name']
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class Department(models.Model):
    """
    Functional departmental division (e.g. Roads & Highways, Bridge Engineering, Electrical & Utilities).
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='departments',
        verbose_name=_('Organization')
    )
    name = models.CharField(max_length=200, verbose_name=_('Department Name'))
    code = models.CharField(max_length=50, verbose_name=_('Department Code'))
    head_of_department = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments',
        verbose_name=_('Head of Department (HOD)')
    )
    budget_allocation = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Allocated Annual Budget ($)')
    )
    description = models.TextField(blank=True, verbose_name=_('Description & Mandate'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return f"{self.name} [{self.organization.code}]"


class Office(models.Model):
    """
    Physical administrative or field operations office.
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='offices',
        verbose_name=_('Organization')
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offices',
        verbose_name=_('Region')
    )
    name = models.CharField(max_length=255, verbose_name=_('Office Name'))
    office_type = models.CharField(
        max_length=50,
        choices=[
            ('HQ', _('Headquarters')),
            ('REGIONAL', _('Regional Directorate')),
            ('DIVISION', _('Division Office')),
            ('FIELD', _('Field Site Office')),
            ('WORKSHOP', _('Maintenance Depot / Workshop')),
        ],
        default='DIVISION',
        verbose_name=_('Office Type')
    )
    address = models.TextField(verbose_name=_('Physical Address'))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_('Phone Contact'))
    email = models.EmailField(blank=True, verbose_name=_('Office Email'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')

    def __str__(self):
        return f"{self.name} ({self.get_office_type_display()})"


class Team(models.Model):
    """
    Operational field or engineering team.
    """
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='teams',
        verbose_name=_('Parent Department')
    )
    office = models.ForeignKey(
        Office,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams',
        verbose_name=_('Base Office')
    )
    name = models.CharField(max_length=200, verbose_name=_('Team Name'))
    code = models.CharField(max_length=50, verbose_name=_('Team Code'))
    team_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_teams',
        verbose_name=_('Team Lead')
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Specialization (e.g. Asphalt Paving, Structural NDT, HVAC)')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    def __str__(self):
        return f"{self.name} ({self.department.name})"
