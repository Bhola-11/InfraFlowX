import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.organizations.models import Organization, Department
from apps.locations.models import Location

class AssetCategory(models.Model):
    """
    Taxonomy classification for infrastructure assets.
    """
    name = models.CharField(max_length=150, unique=True, verbose_name=_('Category Name'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Category Code'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Asset Category')
        verbose_name_plural = _('Asset Categories')

    def __str__(self):
        return f"{self.name} ({self.code})"


class Asset(models.Model):
    """
    Central Asset Registry entity. Tracks lifecycle, conditions, valuations, warranties and locations.
    """
    ASSET_TYPES = [
        ('ROAD', _('Road / Highway Segment')),
        ('BRIDGE', _('Bridge / Overpass')),
        ('BUILDING', _('Building / Structure')),
        ('FACILITY', _('Facility / MEP Plant')),
        ('STREET_INFRA', _('Street & Traffic Infrastructure')),
        ('UTILITY', _('Power / Electrical Utility')),
        ('WATER', _('Water & Drainage Asset')),
        ('HEAVY_EQUIPMENT', _('Heavy Machinery & Fleet')),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', _('Active / Operational')),
        ('UNDER_MAINTENANCE', _('Under Maintenance')),
        ('DAMAGED', _('Damaged / Impaired')),
        ('INACTIVE', _('Inactive / Standby')),
        ('RETIRED', _('Retired / Decommissioned')),
    ]

    CONDITION_CHOICES = [
        ('EXCELLENT', _('Excellent (90-100)')),
        ('GOOD', _('Good (70-89)')),
        ('FAIR', _('Fair (50-69)')),
        ('POOR', _('Poor (25-49)')),
        ('CRITICAL', _('Critical (0-24)')),
    ]

    LIFECYCLE_STAGES = [
        ('PLANNING', _('1. Planning & Design')),
        ('ACQUISITION', _('2. Acquisition & Construction')),
        ('OPERATIONAL', _('3. Active Operation')),
        ('MAINTENANCE', _('4. Overhaul & Major Rehab')),
        ('RETIREMENT', _('5. Retirement Assessment')),
        ('DECOMMISSIONED', _('6. Decommissioned / Scrapped')),
    ]

    DEPRECIATION_METHODS = [
        ('STRAIGHT_LINE', _('Straight-Line Depreciation')),
        ('DECLINING_BALANCE', _('Double Declining Balance')),
        ('NONE', _('Non-Depreciating')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('Official Asset Tag / ID')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Asset Name')
    )
    asset_type = models.CharField(
        max_length=50,
        choices=ASSET_TYPES,
        default='ROAD',
        db_index=True,
        verbose_name=_('Asset Classification')
    )
    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets',
        verbose_name=_('Category')
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='assets',
        verbose_name=_('Owner Organization')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets',
        verbose_name=_('Geospatial Location')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets',
        verbose_name=_('Responsible Department')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_assets',
        verbose_name=_('Custodian / Asset Manager')
    )
    installation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Installation / Commissioning Date')
    )
    acquisition_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Initial Acquisition Cost ($)')
    )
    current_value = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Current Book Value ($)')
    )
    salvage_value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Salvage / Residual Value ($)')
    )
    useful_life_years = models.IntegerField(
        default=25,
        verbose_name=_('Design Useful Life (Years)')
    )
    depreciation_method = models.CharField(
        max_length=50,
        choices=DEPRECIATION_METHODS,
        default='STRAIGHT_LINE',
        verbose_name=_('Depreciation Method')
    )
    condition = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        default='GOOD',
        db_index=True,
        verbose_name=_('Condition Rating')
    )
    condition_score = models.IntegerField(
        default=85,
        verbose_name=_('Condition Score (0–100)')
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        db_index=True,
        verbose_name=_('Operational Status')
    )
    lifecycle_stage = models.CharField(
        max_length=50,
        choices=LIFECYCLE_STAGES,
        default='OPERATIONAL',
        verbose_name=_('Lifecycle Stage')
    )
    warranty_expiry = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Warranty Expiration Date')
    )
    serial_number = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Manufacturer Serial Number')
    )
    barcode = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Barcode / RFID Identifier')
    )
    photo = models.ImageField(
        upload_to='assets/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Asset Photograph')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Technical Description & Notes')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')
        indexes = [
            models.Index(fields=['asset_id']),
            models.Index(fields=['asset_type', 'status']),
            models.Index(fields=['condition_score']),
        ]

    def __str__(self):
        return f"[{self.asset_id}] {self.name} ({self.get_asset_type_display()})"

    def calculate_depreciation(self, elapsed_years):
        """
        Calculates annual depreciation based on useful life and salvage value.
        """
        if self.depreciation_method == 'STRAIGHT_LINE' and self.useful_life_years > 0:
            annual_depreciation = (self.acquisition_cost - self.salvage_value) / Decimal(self.useful_life_years)
            accumulated = annual_depreciation * Decimal(min(elapsed_years, self.useful_life_years))
            return max(self.acquisition_cost - accumulated, self.salvage_value)
        return self.current_value


class AssetStatusHistory(models.Model):
    """
    Audit log of lifecycle status changes for an asset.
    """
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name=_('Asset')
    )
    previous_status = models.CharField(max_length=50, choices=Asset.STATUS_CHOICES)
    new_status = models.CharField(max_length=50, choices=Asset.STATUS_CHOICES)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Operator')
    )
    reason = models.TextField(blank=True, verbose_name=_('Reason for Change'))
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Asset Status History')
        verbose_name_plural = _('Asset Status History Logs')

    def __str__(self):
        return f"{self.asset.asset_id}: {self.previous_status} -> {self.new_status} on {self.timestamp.strftime('%Y-%m-%d')}"
