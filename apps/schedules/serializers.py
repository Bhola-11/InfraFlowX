"""
Schedule Serializers
"""
from apps.schedules.models import AssetSchedule, ScheduledEventExecution


class ScheduleSerializer:
    @staticmethod
    def to_dict(sch):
        return {
            'id': str(sch.id),
            'schedule_code': sch.schedule_code,
            'title': sch.title,
            'schedule_type': sch.schedule_type,
            'schedule_type_display': sch.get_schedule_type_display(),
            'asset_id': sch.asset.asset_id if sch.asset else None,
            'asset_name': sch.asset.name if sch.asset else None,
            'frequency': sch.frequency,
            'frequency_display': sch.get_frequency_display(),
            'next_due_date': sch.next_due_date.isoformat() if sch.next_due_date else None,
            'is_overdue': sch.is_overdue,
            'is_active': sch.is_active,
        }
