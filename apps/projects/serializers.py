"""
Project Serializers
"""
from apps.projects.models import Project, ProjectMilestone


class ProjectSerializer:
    @staticmethod
    def to_dict(proj):
        return {
            'id': str(proj.id),
            'project_id': proj.project_id,
            'name': proj.name,
            'description': proj.description,
            'organization': proj.organization.name if proj.organization else None,
            'project_manager': proj.project_manager.get_full_name() if proj.project_manager else None,
            'contractor': proj.contractor.company_name if proj.contractor else None,
            'start_date': proj.start_date.isoformat() if proj.start_date else None,
            'end_date': proj.end_date.isoformat() if proj.end_date else None,
            'budget': float(proj.budget),
            'actual_spending': float(proj.actual_spending),
            'progress': proj.progress,
            'status': proj.status,
            'status_display': proj.get_status_display(),
            'milestones_count': proj.milestones.count(),
        }
