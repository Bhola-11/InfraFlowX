import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.organizations.models import Organization

class Location(models.Model):
    """
    Hierarchical geospatial location entity with GPS coordinates for GIS-style mapping.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name=_('Organization')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Location Site Name')
    )
    code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Location GIS Code')
    )
    country = models.CharField(max_length=100, default='United States', verbose_name=_('Country'))
    state = models.CharField(max_length=100, verbose_name=_('State / Province'))
    city = models.CharField(max_length=100, verbose_name=_('City / Municipality'))
    district = models.CharField(max_length=100, blank=True, verbose_name=_('District / County'))
    zone = models.CharField(max_length=100, blank=True, verbose_name=_('Operational Zone'))
    area = models.CharField(max_length=150, blank=True, verbose_name=_('Subdivision / Ward / Area'))
    address = models.TextField(verbose_name=_('Full Physical Street Address'))
    postal_code = models.CharField(max_length=30, blank=True, verbose_name=_('Postal / ZIP Code'))
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name=_('Latitude Coordinate')
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name=_('Longitude Coordinate')
    )
    elevation_meters = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Elevation (Meters)')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['city', 'name']
        verbose_name = _('Geospatial Location')
        verbose_name_plural = _('Geospatial Locations')
        indexes = [
            models.Index(fields=['city', 'district']),
            models.Index(fields=['latitude', 'longitude']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state} ({self.code})"

    @property
    def coordinates_display(self):
        return f"{self.latitude:.5f}, {self.longitude:.5f}"
