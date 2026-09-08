"""
Incident Serializers
"""
from apps.incidents.models import Incident, IncidentDispatchLog


class IncidentSerializer:
    @staticmethod
    def to_dict(inc):
        return {
            'id': str(inc.id),
            'incident_id': inc.incident_id,
            'title': inc.title,
            'incident_type': inc.incident_type,
            'incident_type_display': inc.get_incident_type_display(),
            'severity': inc.severity,
            'severity_display': inc.get_severity_display(),
            'status': inc.status,
            'status_display': inc.get_status_display(),
            'asset_id': inc.asset.asset_id if inc.asset else None,
            'location': inc.location.name if inc.location else None,
            'reported_by': inc.reported_by.get_full_name() if inc.reported_by else None,
            'emergency_crew': inc.emergency_crew.name if inc.emergency_crew else None,
            'description': inc.description,
            'estimated_damage_cost': float(inc.estimated_damage_cost),
            'reported_at': inc.reported_at.isoformat() if inc.reported_at else None,
            'resolved_at': inc.resolved_at.isoformat() if inc.resolved_at else None,
        }
