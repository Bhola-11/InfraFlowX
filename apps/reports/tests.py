"""
Comprehensive Unit Tests for Reports App
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.reports.models import ReportTemplate, GeneratedReport
from apps.reports.services import ReportService

User = get_user_model()


class ReportsTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reporter', password='password123')
        self.tpl = ReportTemplate.objects.create(
            code='RPT-TEST-01',
            title='Asset Inventory Export',
            module='ASSETS',
            default_format='CSV'
        )

    def test_report_generation(self):
        gen, csv_data = ReportService.generate_csv_report('RPT-TEST-01', user=self.user)
        self.assertEqual(gen.template, self.tpl)
        self.assertEqual(gen.status, 'COMPLETED')
        self.assertIn('Asset ID', csv_data)
