"""
Management command to capture metric snapshot for executive dashboard.
"""
from django.core.management.base import BaseCommand
from apps.analytics.services import AnalyticsService


class Command(BaseCommand):
    help = 'Captures executive KPI and asset health metric snapshot.'

    def handle(self, *args, **options):
        s = AnalyticsService.capture_metric_snapshot()
        self.stdout.write(self.style.SUCCESS(f"Captured Snapshot: {s.total_assets_count} assets, avg health {s.overall_health_index_avg}%"))
