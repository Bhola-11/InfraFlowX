"""
Analytics Serializers
"""
from apps.analytics.models import DashboardMetricSnapshot, KPITarget, InfrastructureHealthIndex


class AnalyticsSerializer:
    @staticmethod
    def kpi_to_dict(kpi):
        return {
            'id': str(kpi.id),
            'metric_key': kpi.metric_key,
            'name': kpi.name,
            'target_value': float(kpi.target_value),
            'current_actual_value': float(kpi.current_actual_value),
            'unit': kpi.unit,
            'status': kpi.status,
            'is_higher_better': kpi.is_higher_better,
        }
