import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset
from apps.organizations.models import Region

class Road(models.Model):
    """
    Dedicated engineering model for roads, highways, expressways, and urban corridors.
    """
    SURFACE_TYPES = [
        ('ASPHALT', _('Asphalt Pavement')),
        ('CONCRETE', _('Portland Cement Concrete')),
        ('GRAVEL', _('Gravel / Unpaved')),
        ('COMPOSITE', _('Composite Pavement')),
        ('BRICK_PAVER', _('Interlocking Paver Blocks')),
        ('OTHER', _('Other Surface')),
    ]

    TRAFFIC_LEVELS = [
        ('LOW', _('Low (< 2,000 AADT)')),
        ('MEDIUM', _('Medium (2,000 - 10,000 AADT)')),
        ('HIGH', _('High (10,000 - 40,000 AADT)')),
        ('VERY_HIGH', _('Very High (40,000 - 100,000 AADT)')),
        ('CONGESTED', _('Severe Congestion (> 100,000 AADT)')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name='road_extension',
        verbose_name=_('Central Asset Record')
    )
    road_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Official Road Code (e.g. US-101-S)')
    )
    road_name = models.CharField(
        max_length=255,
        verbose_name=_('Corridor / Street Name')
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roads',
        verbose_name=_('Administrative Region')
    )
    length_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Length (Kilometers)')
    )
    width_meters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_('Width (Meters)')
    )
    lanes_count = models.IntegerField(
        default=2,
        verbose_name=_('Number of Traffic Lanes')
    )
    surface_type = models.CharField(
        max_length=50,
        choices=SURFACE_TYPES,
        default='ASPHALT',
        verbose_name=_('Surface Pavement Type')
    )
    construction_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Original Construction Date')
    )
    last_resurfaced_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Last Resurfacing / Overlay Date')
    )
    traffic_level = models.CharField(
        max_length=50,
        choices=TRAFFIC_LEVELS,
        default='MEDIUM',
        verbose_name=_('Average Daily Traffic Level')
    )
    speed_limit_mph = models.IntegerField(
        default=55,
        verbose_name=_('Posted Speed Limit (mph)')
    )
    pci_score = models.IntegerField(
        default=85,
        verbose_name=_('Pavement Condition Index (PCI 0–100)')
    )
    notes = models.TextField(blank=True, verbose_name=_('Engineering Notes'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['road_code']
        verbose_name = _('Road Network')
        verbose_name_plural = _('Road Networks')

    def __str__(self):
        return f"{self.road_code} - {self.road_name} ({self.get_surface_type_display()})"


class RoadDefect(models.Model):
    """
    Field-reported pavement and road surface defects (e.g. Potholes, rutting, cracking).
    """
    DEFECT_TYPES = [
        ('POTHOLE', _('Pothole / Surface Cavity')),
        ('ALLIGATOR_CRACKING', _('Alligator / Fatigue Cracking')),
        ('LONGITUDINAL_CRACK', _('Longitudinal / Transverse Crack')),
        ('RUTTING', _('Wheel Path Rutting')),
        ('RAVELING', _('Raveling / Aggregate Loss')),
        ('DRAINAGE_ISSUE', _('Culvert / Drainage Blockage')),
        ('SUBSIDENCE', _('Subgrade Settlement / Sinkhole')),
        ('GUARDRAIL_DAMAGE', _('Guardrail / Barrier Impact Damage')),
    ]

    SEVERITY_LEVELS = [
        ('LOW', _('Low Severity')),
        ('MEDIUM', _('Medium Severity')),
        ('HIGH', _('High Severity')),
        ('CRITICAL', _('Critical Hazard')),
    ]

    road = models.ForeignKey(
        Road,
        on_delete=models.CASCADE,
        related_name='defects',
        verbose_name=_('Road Corridor')
    )
    defect_type = models.CharField(max_length=50, choices=DEFECT_TYPES, verbose_name=_('Defect Type'))
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='MEDIUM')
    chainage_km = models.DecimalField(max_digits=6, decimal_places=3, verbose_name=_('Chainage / Mile Marker (km)'))
    description = models.TextField(verbose_name=_('Defect Description'))
    photo = models.ImageField(upload_to='defects/roads/%Y/%m/', null=True, blank=True)
    is_repaired = models.BooleanField(default=False)
    reported_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-reported_date']
        verbose_name = _('Road Defect')
        verbose_name_plural = _('Road Defects')

    def __str__(self):
        return f"{self.road.road_code} at KM {self.chainage_km}: {self.get_defect_type_display()} ({self.get_severity_display()})"


class RoadRepairHistory(models.Model):
    """
    Chronological log of paving, resurfacing, patching, and shoulder repairs.
    """
    road = models.ForeignKey(Road, on_delete=models.CASCADE, related_name='repairs')
    repair_title = models.CharField(max_length=255)
    repair_type = models.CharField(max_length=100, default='Milling & Resurfacing')
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    contractor_name = models.CharField(max_length=200, blank=True)
    completion_date = models.DateField()
    pci_gain = models.IntegerField(default=15, verbose_name=_('PCI Score Improvement (+Points)'))
    summary = models.TextField(blank=True)

    class Meta:
        ordering = ['-completion_date']
        verbose_name = _('Road Repair History')
        verbose_name_plural = _('Road Repair Records')

    def __str__(self):
        return f"{self.road.road_code} Repair: {self.repair_title} (${self.cost})"
