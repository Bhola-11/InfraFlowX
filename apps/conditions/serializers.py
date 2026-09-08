"""
Condition Serializers
"""
from apps.conditions.models import ConditionLog, DeteriorationModel


class ConditionSerializer:
    @staticmethod
    def to_dict(clog):
        return {
            'id': clog.id,
            'asset_id': clog.asset.asset_id if clog.asset else None,
            'asset_name': clog.asset.name if clog.asset else None,
            'recorded_date': clog.recorded_date.isoformat() if clog.recorded_date else None,
            'condition_score': clog.condition_score,
            'condition_category': clog.condition_category,
            'condition_category_display': clog.get_condition_category_display(),
            'structural_index': clog.structural_index,
            'operational_index': clog.operational_index,
            'safety_index': clog.safety_index,
            'assessor': clog.assessor.get_full_name() if clog.assessor else None,
            'notes': clog.notes,
        }
