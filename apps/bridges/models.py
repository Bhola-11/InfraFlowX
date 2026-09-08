import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset

class Bridge(models.Model):
    """
    Bridge structural engineering record conforming to National Bridge Inventory (NBI) parameters.
    """
    BRIDGE_TYPES = [
        ('PRESTRESSED_GIRDER', _('Prestressed Concrete Girder / Beam')),
        ('STEEL_TRUSS', _('Steel Truss Bridge')),
        ('SUSPENSION', _('Suspension Bridge')),
        ('CABLE_STAYED', _('Cable-Stayed Bridge')),
        ('CONCRETE_ARCH', _('Reinforced Concrete Arch')),
        ('STEEL_BOX_GIRDER', _('Steel Box Girder')),
        ('CANTILEVER', _('Cantilever Bridge')),
        ('CULVERT', _('Multi-Cell Box Culvert')),
        ('MOVABLE_DRAW', _('Movable / Bascule / Vertical Lift')),
    ]

    CONDITION_CHOICES = [
        ('EXCELLENT', _('Excellent (NBI 9-8)')),
        ('GOOD', _('Good (NBI 7)')),
        ('FAIR', _('Fair (NBI 6-5)')),
        ('POOR', _('Poor (NBI 4)')),
        ('CRITICAL', _('Critical / Structurally Deficient (NBI 3-0)')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name='bridge_extension',
        verbose_name=_('Central Asset Record')
    )
    bridge_id_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Bridge Structure ID (NBI Code)')
    )
    bridge_name = models.CharField(
        max_length=255,
        verbose_name=_('Bridge Name / Feature Carried')
    )
    feature_crossed = models.CharField(
        max_length=200,
        verbose_name=_('Feature Intersected / Waterway / Canyon')
    )
    bridge_type = models.CharField(
        max_length=50,
        choices=BRIDGE_TYPES,
        default='PRESTRESSED_GIRDER',
        verbose_name=_('Structural Type')
    )
    length_meters = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Total Structure Length (Meters)')
    )
    width_meters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_('Deck Width Out-to-Out (Meters)')
    )
    span_count = models.IntegerField(
        default=1,
        verbose_name=_('Number of Main Spans')
    )
    main_span_length = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Maximum Span Length (Meters)')
    )
    construction_year = models.IntegerField(
        verbose_name=_('Original Year Built')
    )
    load_capacity_tons = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=40.00,
        verbose_name=_('Design Live Load Capacity (Tons)')
    )
    vertical_clearance_meters = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Under-Clearance (Meters)')
    )
    condition = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        default='GOOD',
        verbose_name=_('Structural Condition Rating')
    )
    inspection_frequency_months = models.IntegerField(
        default=24,
        verbose_name=_('Mandatory Inspection Frequency (Months)')
    )
    is_scour_critical = models.BooleanField(
        default=False,
        verbose_name=_('Scour Critical Waterway Foundation')
    )
    notes = models.TextField(blank=True, verbose_name=_('Structural Engineering Notes'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['bridge_id_code']
        verbose_name = _('Bridge Structure')
        verbose_name_plural = _('Bridge Structures')

    def __str__(self):
        return f"{self.bridge_id_code} - {self.bridge_name} ({self.get_bridge_type_display()})"


class BridgeComponentInspection(models.Model):
    """
    Sub-component health ratings (Deck, Superstructure, Substructure, Piers, Bearings).
    """
    COMPONENT_CHOICES = [
        ('DECK', _('Bridge Deck & Wearing Surface')),
        ('SUPERSTRUCTURE', _('Superstructure Girders / Trusses')),
        ('SUBSTRUCTURE', _('Substructure Abutments & Piers')),
        ('BEARINGS', _('Elastomeric / Pot Bearings')),
        ('EXPANSION_JOINTS', _('Expansion Joints & Seals')),
        ('CULVERT_BARREL', _('Culvert Barrel / Headwalls')),
        ('SCOUR_PROTECTION', _('Riprap & Scour Countermeasures')),
    ]

    bridge = models.ForeignKey(Bridge, on_delete=models.CASCADE, related_name='components')
    component = models.CharField(max_length=50, choices=COMPONENT_CHOICES)
    rating_score_1_to_9 = models.IntegerField(
        default=7,
        verbose_name=_('NBI Component Rating (1=Failed to 9=Excellent)')
    )
    findings = models.TextField(blank=True)
    photo = models.ImageField(upload_to='bridges/components/%Y/%m/', null=True, blank=True)
    inspected_date = models.DateField()

    class Meta:
        ordering = ['-inspected_date']
        verbose_name = _('Bridge Component Inspection')
        verbose_name_plural = _('Bridge Component Inspections')

    def __str__(self):
        return f"{self.bridge.bridge_id_code} - {self.get_component_display()}: Rating {self.rating_score_1_to_9}/9"
