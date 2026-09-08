"""
Building Serializers
"""
from apps.buildings.models import Building, BuildingFloor


class BuildingSerializer:
    @staticmethod
    def to_dict(bldg):
        return {
            'id': str(bldg.id),
            'building_id_code': bldg.building_id_code,
            'building_name': bldg.building_name,
            'building_type': bldg.building_type,
            'building_type_display': bldg.get_building_type_display(),
            'address': bldg.address,
            'floor_count': bldg.floor_count,
            'total_area_sqft': float(bldg.total_area_sqft),
            'construction_year': bldg.construction_year,
            'occupancy_capacity': bldg.occupancy_capacity,
            'energy_rating': bldg.energy_rating,
            'energy_rating_display': bldg.get_energy_rating_display(),
            'is_fire_safety_certified': bldg.is_fire_safety_certified,
            'asset_id': bldg.asset.asset_id if bldg.asset else None,
            'floors_count': bldg.floors.count(),
        }

    @staticmethod
    def floor_to_dict(floor):
        return {
            'id': floor.id,
            'building_code': floor.building.building_id_code,
            'floor_number': floor.floor_number,
            'floor_name': floor.floor_name,
            'area_sqft': float(floor.area_sqft),
            'usage_type': floor.usage_type,
        }
