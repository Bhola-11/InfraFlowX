"""
Facility Serializers
"""
from apps.facilities.models import FacilityEquipment, FacilityServiceLog


class FacilitySerializer:
    @staticmethod
    def to_dict(eq):
        return {
            'id': str(eq.id),
            'equipment_code': eq.equipment_code,
            'equipment_name': eq.equipment_name,
            'equipment_type': eq.equipment_type,
            'equipment_type_display': eq.get_equipment_type_display(),
            'manufacturer': eq.manufacturer,
            'model_number': eq.model_number,
            'power_rating_kw': float(eq.power_rating_kw) if eq.power_rating_kw else None,
            'operating_hours': float(eq.operating_hours),
            'last_service_date': eq.last_service_date.isoformat() if eq.last_service_date else None,
            'asset_id': eq.asset.asset_id if eq.asset else None,
            'service_logs_count': eq.service_logs.count(),
        }

    @staticmethod
    def service_log_to_dict(log):
        return {
            'id': log.id,
            'equipment_code': log.equipment.equipment_code,
            'service_type': log.service_type,
            'service_type_display': log.get_service_type_display(),
            'service_date': log.service_date.isoformat() if log.service_date else None,
            'cost': float(log.cost),
            'performed_by': log.performed_by,
            'downtime_hours': float(log.downtime_hours),
            'description': log.description,
        }
