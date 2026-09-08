"""
Comprehensive Unit Tests for Organizations App
"""
from decimal import Decimal
from django.test import TestCase
from apps.organizations.models import Organization, Department, Office, Team
from apps.organizations.services import OrganizationService


class OrganizationsTestSuite(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            name='State Transport Ministry',
            code='STM-HQ',
            annual_budget=Decimal('2500000000.00')
        )
        self.dept = Department.objects.create(organization=self.org, name='Bridges Wing', code='DEP-BRG')
        self.office = Office.objects.create(organization=self.org, name='Capital Regional Office', office_type='HEADQUARTERS')
        self.team = Team.objects.create(department=self.dept, office=self.office, name='Cable Inspection Alpha', code='TEAM-CBL')

    def test_org_summary(self):
        s = OrganizationService.get_organization_summary(self.org.id)
        self.assertEqual(s['organization_name'], self.org.name)
        self.assertEqual(s['departments_count'], 1)
        self.assertEqual(s['offices_count'], 1)
