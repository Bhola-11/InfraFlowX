"""
Facility Equipment Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.facilities.models import FacilityEquipment, FacilityServiceLog
from apps.facilities.engineering import EquipmentReliabilityEngine
from apps.audit.utils import log_audit_event


class FacilityService:
    @staticmethod
    def compute_equipment_health(equipment_id):
        eq = FacilityEquipment.objects.prefetch_related('service_logs').get(id=equipment_id)
        logs = list(eq.service_logs.all())
        failure_count = max(1, len(logs))
        total_downtime = failure_count * 8.0
        
        metrics = EquipmentReliabilityEngine.calculate_mtbf_mttr(
            total_operating_hours=eq.operating_hours,
            failure_count=failure_count,
            total_downtime_hours=total_downtime
        )
        return {
            'equipment_code': eq.equipment_code,
            'equipment_name': eq.equipment_name,
            'operating_hours': eq.operating_hours,
            'metrics': metrics,
            'total_service_events': len(logs)
        }

    @staticmethod
    @transaction.atomic
    def record_service_intervention(equipment, service_type, service_date, cost, technician_name, notes="", operating_hours=None, user=None):
        log = FacilityServiceLog.objects.create(
            equipment=equipment,
            service_type=service_type,
            service_date=service_date,
            cost=cost,
            technician_name=technician_name,
            operating_hours_at_service=operating_hours or equipment.operating_hours,
            notes=notes
        )
        equipment.last_service_date = service_date
        equipment.save(update_fields=['last_service_date'])
        
        log_audit_event(
            action='MAINTENANCE_ACTION',
            module='facilities',
            object_id=str(log.id),
            object_repr=str(log),
            description=f"Service {service_type} logged on equipment {equipment.equipment_code}. Cost: ${cost:,}",
            user=user
        )
        return log
