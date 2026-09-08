"""
InfraFlowX - GIS GeoJSON & KML Infrastructure Spatial Export Engine
Builds standard GeoJSON FeatureCollections and KML placemarks for GIS mapping.
"""

from typing import Dict, List, Any
import json


class GISExportEngine:
    """
    Exports infrastructure asset records to standardized GeoJSON format.
    """

    @classmethod
    def build_geojson_feature_collection(cls, assets_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        features = []
        for asset in assets_data:
            lat = asset.get("latitude")
            lon = asset.get("longitude")
            if lat is None or lon is None:
                continue

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(lon), float(lat)]
                },
                "properties": {
                    "id": asset.get("id"),
                    "name": asset.get("name", ""),
                    "asset_type": asset.get("asset_type", ""),
                    "condition_score": asset.get("condition_score", 100),
                    "status": asset.get("status", "OPERATIONAL"),
                }
            }
            features.append(feature)

        return {
            "type": "FeatureCollection",
            "features": features,
            "total_features": len(features),
        }
