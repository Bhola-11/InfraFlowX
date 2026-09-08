"""
Comprehensive Unit Tests for Employees App
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization, Department, Office, Team
from apps.employees.models import Designation, Employee
from apps.employees.services import EmployeeService

User = get_user_model()


class EmployeesTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='emp_user', password='password123', first_name='Vikram', last_name='Mehta')
        self.org = Organization.objects.create(name='Civil Works', code='CW-01')
        self.dept = Department.objects.create(organization=self.org, name='Roads', code='RD')
        self.office = Office.objects.create(organization=self.org, name='North Hub')
        self.desig = Designation.objects.create(title='Lead Pavement Engineer', code='DES-PAVE')
        self.emp = Employee.objects.create(
            user=self.user,
            employee_id='EMP-0099',
            organization=self.org,
            department=self.dept,
            office=self.office,
            designation=self.desig,
            status='ACTIVE',
            date_of_joining='2020-01-15'
        )

    def test_employee_workload(self):
        w = EmployeeService.get_employee_workload(self.emp.id)
        self.assertEqual(w['employee_name'], 'Vikram Mehta')
        self.assertEqual(w['designation'], 'Lead Pavement Engineer')
