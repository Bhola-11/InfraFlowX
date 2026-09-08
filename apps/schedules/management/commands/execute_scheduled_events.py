"""
Management command to trigger pending scheduled PM events.
"""
from django.core.management.base import BaseCommand
from apps.schedules.services import ScheduleService


class Command(BaseCommand):
    help = 'Triggers due scheduled maintenance and audit events.'

    def handle(self, *args, **options):
        events = ScheduleService.trigger_scheduled_executions()
        self.stdout.write(self.style.SUCCESS(f"Triggered {len(events)} recurring schedule executions."))
