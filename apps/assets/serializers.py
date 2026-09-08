"""
Asset Serializers
"""
from apps.assets.models import Asset, AssetCategory, AssetStatusHistory


class AssetSerializer:
    @staticmethod
    def to_dict(asset):
        return {
            'id': str(asset.id),
            'asset_id': asset.asset_id,
            'name': asset.name,
            'asset_type': asset.asset_type,
            'asset_type_display': asset.get_asset_type_display(),
            'category': asset.category.name if asset.category else None,
            'organization': asset.organization.name if asset.organization else None,
            'department': asset.department.name if asset.department else None,
            'location': asset.location.name if asset.location else None,
            'status': asset.status,
            'status_display': asset.get_status_display(),
            'condition': asset.condition,
            'condition_display': asset.get_condition_display(),
            'condition_score': asset.condition_score,
            'acquisition_cost': float(asset.acquisition_cost),
            'current_value': float(asset.current_value),
            'installation_date': asset.installation_date.isoformat() if asset.installation_date else None,
            'useful_life_years': asset.useful_life_years,
            'description': asset.description,
        }

    @staticmethod
    def to_geojson(asset):
        if not asset.location or not asset.location.latitude or not asset.location.longitude:
            return None
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(asset.location.longitude), float(asset.location.latitude)]
            },
            'properties': {
                'id': str(asset.id),
                'asset_id': asset.asset_id,
                'name': asset.name,
                'type': asset.asset_type,
                'status': asset.status,
                'condition_score': asset.condition_score,
                'location_name': asset.location.name,
            }
        }
