"""
Building Management Services
"""
from decimal import Decimal
from django.db import transaction
from apps.buildings.models import Building, BuildingFloor
from apps.buildings.engineering import FacilityConditionIndexEngine, BuildingEnergyEngine
from apps.audit.utils import log_audit_event


class BuildingService:
    @staticmethod
    def evaluate_building_fci(building_id, estimated_repair_cost=None):
        bldg = Building.objects.select_related('asset').get(id=building_id)
        crv = bldg.asset.acquisition_cost if (bldg.asset and bldg.asset.acquisition_cost > 0) else (bldg.total_area_sqft * Decimal('350.00'))
        repair_cost = estimated_repair_cost or Decimal('250000.00')
        
        fci = FacilityConditionIndexEngine.calculate_fci(repair_cost, crv)
        status_info = FacilityConditionIndexEngine.get_fci_status(fci)
        
        return {
            'building_code': bldg.building_id_code,
            'building_name': bldg.building_name,
            'current_replacement_value': crv,
            'repair_needs': repair_cost,
            'fci_score': fci,
            'fci_status': status_info
        }

    @staticmethod
    @transaction.atomic
    def add_floor(building, floor_number, floor_name, area_sqft, usage_type, user=None):
        floor = BuildingFloor.objects.create(
            building=building,
            floor_number=floor_number,
            floor_name=floor_name,
            area_sqft=area_sqft,
            usage_type=usage_type
        )
        
        log_audit_event(
            action='CREATE',
            module='buildings',
            object_id=str(floor.id),
            object_repr=str(floor),
            description=f"Floor {floor_number} ({floor_name}) registered in {building.building_name}",
            user=user
        )
        return floor
