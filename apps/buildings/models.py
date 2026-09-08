import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset

class Building(models.Model):
    """
    Municipal and infrastructure public facility buildings.
    """
    BUILDING_TYPES = [
        ('OFFICE', _('Administrative / Headquarters Office')),
        ('SCHOOL', _('Educational / School / University')),
        ('HOSPITAL', _('Healthcare / Hospital / Clinic')),
        ('WAREHOUSE', _('Warehouse / Logistics Depot')),
        ('GOVERNMENT', _('Government / Civic Center / Courthouse')),
        ('EMERGENCY_SERVICES', _('Fire Station / Police Depot / EMS')),
        ('TRANSIT_TERMINAL', _('Transit Station / Airport Terminal')),
        ('RESIDENTIAL', _('Public / Municipal Housing')),
        ('COMMERCIAL', _('Commercial Facility')),
        ('OTHER', _('Other Structure')),
    ]

    ENERGY_RATINGS = [
        ('LEED_PLATINUM', _('LEED Platinum')),
        ('LEED_GOLD', _('LEED Gold')),
        ('LEED_SILVER', _('LEED Silver')),
        ('ENERGY_STAR', _('Energy Star Certified')),
        ('STANDARD', _('Standard Municipal Code')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name='building_extension',
        verbose_name=_('Central Asset Record')
    )
    building_id_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Building ID Code')
    )
    building_name = models.CharField(
        max_length=255,
        verbose_name=_('Building Name')
    )
    building_type = models.CharField(
        max_length=50,
        choices=BUILDING_TYPES,
        default='OFFICE',
        verbose_name=_('Building Classification')
    )
    address = models.TextField(verbose_name=_('Physical Address'))
    floor_count = models.IntegerField(default=1, verbose_name=_('Number of Floors'))
    total_area_sqft = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Total Gross Floor Area (sq ft)')
    )
    construction_year = models.IntegerField(verbose_name=_('Year Built'))
    occupancy_capacity = models.IntegerField(default=100, verbose_name=_('Maximum Occupancy Capacity'))
    energy_rating = models.CharField(
        max_length=50,
        choices=ENERGY_RATINGS,
        default='STANDARD',
        verbose_name=_('Energy & Sustainability Rating')
    )
    is_fire_safety_certified = models.BooleanField(
        default=True,
        verbose_name=_('Fire & Life Safety Certified')
    )
    hvac_system_type = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Central HVAC / Chiller Specification')
    )
    roof_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Roofing System (e.g. Built-Up Membrane, Metal)')
    )
    notes = models.TextField(blank=True, verbose_name=_('Facility Engineering Notes'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['building_id_code']
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')

    def __str__(self):
        return f"{self.building_id_code} - {self.building_name} ({self.get_building_type_display()})"


class BuildingFloor(models.Model):
    """
    Subdivision of building levels, zones, and room capacity.
    """
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField(default=1)
    floor_name = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 2nd Floor Engineering Wing")
    area_sqft = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    usage_type = models.CharField(max_length=100, default='Office Space')

    class Meta:
        ordering = ['floor_number']
        verbose_name = _('Building Floor')
        verbose_name_plural = _('Building Floors')

    def __str__(self):
        return f"{self.building.building_id_code} - Floor {self.floor_number}: {self.floor_name}"
