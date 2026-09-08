"""
Incident Management & Emergency Dispatch Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.incidents.models import Incident, IncidentDispatchLog
from apps.audit.utils import log_audit_event
from apps.notifications.utils import send_notification


class IncidentService:
    @staticmethod
    @transaction.atomic
    def dispatch_emergency_crew(incident_id, responder_name, action_taken, user=None):
        inc = Incident.objects.get(id=incident_id)
        inc.status = 'DISPATCHED'
        inc.save(update_fields=['status'])
        
        log = IncidentDispatchLog.objects.create(
            incident=inc,
            responder_name=responder_name,
            action_taken=action_taken
        )
        
        log_audit_event(
            action='UPDATE',
            module='incidents',
            object_id=str(inc.id),
            object_repr=str(inc),
            description=f"Crew dispatched to incident {inc.incident_id}: {responder_name}",
            user=user
        )
        return log

    @staticmethod
    @transaction.atomic
    def resolve_incident(incident_id, resolution_summary, root_cause="", user=None):
        inc = Incident.objects.get(id=incident_id)
        inc.status = 'RESOLVED'
        inc.resolution_summary = resolution_summary
        inc.root_cause_analysis = root_cause
        inc.resolved_at = timezone.now()
        inc.save(update_fields=['status', 'resolution_summary', 'root_cause_analysis', 'resolved_at'])
        
        log_audit_event(
            action='UPDATE',
            module='incidents',
            object_id=str(inc.id),
            object_repr=str(inc),
            description=f"Incident {inc.incident_id} marked RESOLVED",
            user=user
        )
        return inc
