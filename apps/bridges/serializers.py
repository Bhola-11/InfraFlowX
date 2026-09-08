"""
Bridge Serializers & Data Transfer Objects
"""
from apps.bridges.models import Bridge, BridgeComponentInspection


class BridgeSerializer:
    @staticmethod
    def to_dict(bridge):
        return {
            'id': str(bridge.id),
            'bridge_id_code': bridge.bridge_id_code,
            'bridge_name': bridge.bridge_name,
            'feature_crossed': bridge.feature_crossed,
            'bridge_type': bridge.bridge_type,
            'bridge_type_display': bridge.get_bridge_type_display(),
            'length_meters': float(bridge.length_meters),
            'width_meters': float(bridge.width_meters),
            'span_count': bridge.span_count,
            'main_span_length': float(bridge.main_span_length) if bridge.main_span_length else None,
            'construction_year': bridge.construction_year,
            'load_capacity_tons': float(bridge.load_capacity_tons),
            'vertical_clearance_meters': float(bridge.vertical_clearance_meters) if bridge.vertical_clearance_meters else None,
            'condition': bridge.condition,
            'condition_display': bridge.get_condition_display(),
            'is_scour_critical': bridge.is_scour_critical,
            'asset_id': bridge.asset.asset_id if bridge.asset else None,
            'components_count': bridge.components.count(),
        }

    @staticmethod
    def component_to_dict(comp):
        return {
            'id': comp.id,
            'bridge_code': comp.bridge.bridge_id_code,
            'component': comp.component,
            'component_display': comp.get_component_display(),
            'rating_score_1_to_9': comp.rating_score_1_to_9,
            'findings': comp.findings,
            'inspected_date': comp.inspected_date.isoformat() if comp.inspected_date else None,
        }
