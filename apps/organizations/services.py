"""
Organization & Hierarchy Services
"""
from apps.organizations.models import Organization, Department, Office, Team


class OrganizationService:
    @staticmethod
    def get_organization_summary(org_id):
        org = Organization.objects.prefetch_related('departments', 'offices', 'contractors', 'projects').get(id=org_id)
        return {
            'organization_name': org.name,
            'departments_count': org.departments.count(),
            'offices_count': org.offices.count(),
            'active_projects_count': org.projects.filter(status='ACTIVE').count(),
            'annual_budget': float(org.annual_budget),
        }
