"""
Comprehensive Unit Tests for Schedules App
"""
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from apps.organizations.models import Organization
from apps.assets.models import AssetCategory, Asset
from apps.schedules.models import AssetSchedule, ScheduledEventExecution
from apps.schedules.services import ScheduleService


class SchedulesTestSuite(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Highways Agency', code='HA-01')
        self.cat = AssetCategory.objects.create(name='Bridges', code='CAT-BRG')
        self.asset = Asset.objects.create(
            asset_id='AST-SCH-01',
            name='River Bridge Pylon',
            asset_type='BRIDGE',
            category=self.cat,
            organization=self.org
        )
        self.sch = AssetSchedule.objects.create(
            schedule_code='SCH-TEST-01',
            title='Stay Cable Tension Calibration',
            schedule_type='STATUTORY_AUDIT',
            asset=self.asset,
            organization=self.org,
            frequency='MONTHLY',
            start_date=timezone.now().date(),
            next_due_date=timezone.now().date(),
            auto_generate_workorder=True
        )

    def test_trigger_scheduled_executions(self):
        triggered = ScheduleService.trigger_scheduled_executions()
        self.assertGreaterEqual(len(triggered), 1)
        self.sch.refresh_from_db()
        self.assertTrue(self.sch.next_due_date > timezone.now().date())
