"""
Project Management Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.projects.models import Project, ProjectMilestone
from apps.projects.engineering import EVMEngine
from apps.audit.utils import log_audit_event


class ProjectService:
    @staticmethod
    def compute_project_evm(project_id):
        proj = Project.objects.prefetch_related('milestones').get(id=project_id)
        evm = EVMEngine.calculate_evm_metrics(
            budget_at_completion=proj.budget,
            actual_cost=proj.actual_spending,
            progress_percentage=proj.progress,
            planned_percentage=50
        )
        return {
            'project_id': proj.project_id,
            'name': proj.name,
            'status': proj.status,
            'progress': proj.progress,
            'evm': evm
        }

    @staticmethod
    @transaction.atomic
    def mark_milestone_completed(milestone_id, completed_date=None, user=None):
        m = ProjectMilestone.objects.select_related('project').get(id=milestone_id)
        m.is_completed = True
        m.completed_date = completed_date or timezone.now().date()
        m.save(update_fields=['is_completed', 'completed_date'])
        
        # Recalculate project progress
        proj = m.project
        all_milestones = proj.milestones.all()
        total_weight = sum(ms.weight_percentage for ms in all_milestones)
        completed_weight = sum(ms.weight_percentage for ms in all_milestones if ms.is_completed)
        
        if total_weight > 0:
            proj.progress = int((completed_weight / total_weight) * 100)
            proj.save(update_fields=['progress'])
            
        log_audit_event(
            action='PROJECT_CHANGE',
            module='projects',
            object_id=str(m.id),
            object_repr=str(m),
            description=f"Milestone '{m.milestone_title}' completed on project {proj.project_id}",
            user=user
        )
        return m
