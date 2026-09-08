import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset

class FacilityEquipment(models.Model):
    """
    Facility MEP mechanical, electrical, plumbing, generator, and elevator equipment.
    """
    EQUIPMENT_TYPES = [
        ('HVAC_CHILLER', _('HVAC Central Chiller / AHU')),
        ('ELEVATOR_LIFT', _('Passenger / Freight Elevator')),
        ('DIESEL_GENERATOR', _('Emergency Diesel Generator')),
        ('ELECTRICAL_TRANSFORMER', _('Substation Transformer & Switchgear')),
        ('PLUMBING_PUMP', _('Water Pressure Booster Pump Station')),
        ('FIRE_SUPPRESSION', _('Fire Sprinkler & Deluge System')),
        ('SECURITY_CCTV', _('Access Control & CCTV Surveillance')),
        ('SOLAR_INVERTER', _('Solar Photovoltaic Inverter')),
        ('BOILER', _('High Pressure Steam Boiler')),
        ('OTHER', _('General Facility Asset')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name='facility_extension',
        verbose_name=_('Central Asset Record')
    )
    equipment_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Equipment Serial Tag')
    )
    equipment_name = models.CharField(
        max_length=255,
        verbose_name=_('Equipment Unit Name')
    )
    equipment_type = models.CharField(
        max_length=50,
        choices=EQUIPMENT_TYPES,
        default='HVAC_CHILLER',
        verbose_name=_('Equipment Classification')
    )
    manufacturer = models.CharField(max_length=150, blank=True, verbose_name=_('Original Manufacturer'))
    model_number = models.CharField(max_length=100, blank=True, verbose_name=_('Model / Part Number'))
    power_rating_kw = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Power Rating (kW / kVA)')
    )
    operating_hours = models.DecimalField(
        max_digits=9,
        decimal_places=1,
        default=0.0,
        verbose_name=_('Cumulative Run Hours')
    )
    last_service_date = models.DateField(null=True, blank=True, verbose_name=_('Last Serviced Date'))
    next_service_due = models.DateField(null=True, blank=True, verbose_name=_('Next Service Due Date'))
    service_contract_vendor = models.CharField(max_length=200, blank=True, verbose_name=_('SLA Service Vendor'))
    telemetry_data = models.JSONField(default=dict, blank=True, verbose_name=_('Sensor Telemetry Readings'))
    notes = models.TextField(blank=True, verbose_name=_('Maintenance Notes'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['equipment_code']
        verbose_name = _('Facility Equipment')
        verbose_name_plural = _('Facility Equipment & MEP')

    def __str__(self):
        return f"{self.equipment_code} - {self.equipment_name} ({self.get_equipment_type_display()})"


class FacilityServiceLog(models.Model):
    """
    Log of maintenance service dispatches and part replacements for facility plant.
    """
    SERVICE_TYPES = [
        ('PREVENTIVE_MAINTENANCE', _('Scheduled Preventive Service')),
        ('EMERGENCY_REPAIR', _('Emergency Breakdown Repair')),
        ('PARTS_REPLACEMENT', _('Component / Filter Replacement')),
        ('ANNUAL_OVERHAUL', _('Comprehensive Annual Overhaul')),
        ('SAFETY_INSPECTION', _('Compliance & Safety Audit')),
    ]

    equipment = models.ForeignKey(FacilityEquipment, on_delete=models.CASCADE, related_name='service_logs')
    service_date = models.DateField()
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, default='PREVENTIVE_MAINTENANCE')
    technician_name = models.CharField(max_length=150)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    operating_hours_at_service = models.DecimalField(max_digits=9, decimal_places=1, default=0.0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-service_date']
        verbose_name = _('Facility Service Log')
        verbose_name_plural = _('Facility Service Logs')

    def __str__(self):
        return f"{self.equipment.equipment_code} Serviced: {self.get_service_type_display()} on {self.service_date}"
