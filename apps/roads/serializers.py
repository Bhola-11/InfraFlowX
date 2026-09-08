"""
Roads Serializers & JSON Formatters
"""
from apps.roads.models import Road, RoadDefect, RoadRepairHistory


class RoadSerializer:
    @staticmethod
    def to_dict(road):
        return {
            'id': str(road.id),
            'road_code': road.road_code,
            'road_name': road.road_name,
            'region': road.region.name if road.region else None,
            'length_km': float(road.length_km),
            'width_meters': float(road.width_meters),
            'lanes_count': road.lanes_count,
            'surface_type': road.surface_type,
            'surface_type_display': road.get_surface_type_display(),
            'traffic_level': road.traffic_level,
            'speed_limit_mph': road.speed_limit_mph,
            'pci_score': road.pci_score,
            'asset_id': road.asset.asset_id if road.asset else None,
            'active_defects_count': road.defects.filter(is_repaired=False).count(),
        }

    @staticmethod
    def defect_to_dict(defect):
        return {
            'id': defect.id,
            'road_code': defect.road.road_code,
            'defect_type': defect.defect_type,
            'defect_type_display': defect.get_defect_type_display(),
            'severity': defect.severity,
            'chainage_km': float(defect.chainage_km),
            'description': defect.description,
            'is_repaired': defect.is_repaired,
            'reported_date': defect.reported_date.isoformat() if defect.reported_date else None,
        }
