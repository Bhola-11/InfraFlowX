import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.assets.models import Asset
from apps.locations.models import Location
from apps.organizations.models import Team

class Incident(models.Model):
    """
    Emergency incident, safety hazard, public impairment, and disaster dispatch ticket.
    """
    INCIDENT_TYPES = [
        ('STRUCTURAL_DAMAGE', _('Structural Failure / Collapse Risk')),
        ('ROAD_HAZARD', _('Road Subsidence / Sinkhole / Severe Pothole')),
        ('EQUIPMENT_BREAKDOWN', _('Plant Equipment / Chiller / Lift Failure')),
        ('SAFETY_VIOLATION', _('Occupational Safety & Site Hazard')),
        ('ENVIRONMENTAL_SPILL', _('Chemical / Hazardous Material Spill')),
        ('FLOOD_WATERLOGGING', _('Severe Flooding & Stormwater Overflow')),
        ('POWER_OUTAGE', _('Substation Outage / Grid Fault')),
        ('CITIZEN_COMPLAINT', _('Citizen Public Works Grievance')),
    ]

    SEVERITY_LEVELS = [
        ('LOW', _('Low (Informational / Non-Urgent)')),
        ('MEDIUM', _('Medium (Operational Impairment)')),
        ('HIGH', _('High (Imminent Safety Hazard)')),
        ('CRITICAL', _('Critical Disaster / Emergency Response')),
    ]

    STATUS_CHOICES = [
        ('REPORTED', _('Reported / Pending Triage')),
        ('DISPATCHED', _('Emergency Response Crew Dispatched')),
        ('UNDER_INVESTIGATION', _('Under On-Site Investigation')),
        ('CONTAINED', _('Hazard Contained / Safe')),
        ('RESOLVED', _('Fully Resolved & Repaired')),
        ('CLOSED', _('Closed & Archived')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name=_('Incident Ticket Number')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Incident Title / Headline')
    )
    incident_type = models.CharField(
        max_length=50,
        choices=INCIDENT_TYPES,
        default='ROAD_HAZARD',
        verbose_name=_('Incident Classification')
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_LEVELS,
        default='HIGH',
        db_index=True,
        verbose_name=_('Severity Level')
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidents',
        verbose_name=_('Impaired Infrastructure Asset')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidents',
        verbose_name=_('Geospatial Location')
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reported_incidents',
        verbose_name=_('Reporting Officer / Citizen')
    )
    emergency_crew = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dispatched_incidents',
        verbose_name=_('Dispatched Emergency Response Team')
    )
    description = models.TextField(
        verbose_name=_('Detailed Incident Narrative & Damage Description')
    )
    estimated_damage_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Estimated Damage / Repair Cost ($)')
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='REPORTED',
        db_index=True,
        verbose_name=_('Incident Status')
    )
    root_cause_analysis = models.TextField(
        blank=True,
        verbose_name=_('Root Cause Analysis (RCA)')
    )
    resolution_summary = models.TextField(
        blank=True,
        verbose_name=_('Corrective Action Resolution Summary')
    )
    photo_evidence = models.ImageField(
        upload_to='incidents/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Incident Scene Photograph')
    )
    reported_at = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-reported_at']
        verbose_name = _('Incident')
        verbose_name_plural = _('Incidents & Hazards')
        indexes = [
            models.Index(fields=['incident_id']),
            models.Index(fields=['status', 'severity', '-reported_at']),
        ]

    def __str__(self):
        return f"[{self.incident_id}] {self.title} ({self.get_severity_display()}) - {self.get_status_display()}"


class IncidentDispatchLog(models.Model):
    """
    Timeline log of field crew dispatches, on-scene arrivals, and triage updates.
    """
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name='dispatch_logs',
        verbose_name=_('Incident Ticket')
    )
    responder_name = models.CharField(max_length=150, verbose_name=_('Responder / Officer Name'))
    action_taken = models.TextField(verbose_name=_('Containment Action Taken'))
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Incident Dispatch Log')
        verbose_name_plural = _('Incident Dispatch Logs')

    def __str__(self):
        return f"{self.incident.incident_id}: {self.responder_name} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
