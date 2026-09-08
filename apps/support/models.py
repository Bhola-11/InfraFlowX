import uuid
from django.db import models
from django.conf import settings
from apps.organizations.models import Department
from apps.assets.models import Asset
from apps.locations.models import Location


class SLAPolicy(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical / Emergency'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, unique=True)
    response_time_hours = models.PositiveIntegerField(default=24)
    resolution_time_hours = models.PositiveIntegerField(default=72)
    escalation_email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['priority']
        verbose_name = 'SLA Policy'
        verbose_name_plural = 'SLA Policies'

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()}: {self.resolution_time_hours}h)"


class SupportTicket(models.Model):
    CATEGORY_CHOICES = [
        ('INFRA_DAMAGE', 'Physical Infrastructure Damage'),
        ('POTHOLE_HAZARD', 'Pothole / Roadway Surface Hazard'),
        ('STREETLIGHT_FAILURE', 'Streetlight / Lighting Outage'),
        ('WATERLOGGING', 'Drainage / Waterlogging Issue'),
        ('BRIDGE_CRACK', 'Bridge Expansion / Crack Report'),
        ('PUBLIC_NUISANCE', 'Public Safety / Obstruction'),
        ('GENERAL_QUERY', 'General Public Inquiry'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical / Emergency'),
    ]

    STATUS_CHOICES = [
        ('NEW', 'New / Unassigned'),
        ('ASSIGNED', 'Assigned to Team'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
        ('REJECTED', 'Rejected / Invalid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=60, unique=True)
    subject = models.CharField(max_length=255)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='POTHOLE_HAZARD')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets')
    reporter_name = models.CharField(max_length=150)
    reporter_email = models.EmailField(blank=True, null=True)
    reporter_phone = models.CharField(max_length=30, blank=True, null=True)
    is_citizen_complaint = models.BooleanField(default=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_support_tickets')
    assigned_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets')
    description = models.TextField()
    resolution_notes = models.TextField(blank=True, null=True)
    resolution_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'

    def __str__(self):
        return f"{self.ticket_number} - {self.subject} [{self.get_status_display()}]"


class TicketComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=150, blank=True, null=True)
    comment = models.TextField()
    is_internal_note = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Ticket Comment'
        verbose_name_plural = 'Ticket Comments'

    def __str__(self):
        return f"Comment on {self.ticket.ticket_number} by {self.author or self.author_name}"


class CitizenFeedback(models.Model):
    RATING_CHOICES = [(i, f"{i} Stars") for i in range(1, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.OneToOneField(SupportTicket, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Citizen Feedback'
        verbose_name_plural = 'Citizen Feedbacks'

    def __str__(self):
        return f"Rating {self.rating} for {self.ticket.ticket_number}"
