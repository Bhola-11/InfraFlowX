"""
Contractor Management Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.contractors.models import Contractor, ContractAgreement, ContractorEvaluation
from apps.audit.utils import log_audit_event


class ContractorService:
    @staticmethod
    @transaction.atomic
    def submit_evaluation(contractor, quality_score, safety_score, timeliness_score, comments="", evaluated_by=None):
        overall = Decimal(str((quality_score + safety_score + timeliness_score) / 3.0))
        eval_record = ContractorEvaluation.objects.create(
            contractor=contractor,
            evaluated_by=evaluated_by,
            quality_score=quality_score,
            safety_score=safety_score,
            timeliness_score=timeliness_score,
            overall_score=round(overall, 2),
            comments=comments
        )
        
        # Update contractor running average rating
        evals = contractor.evaluations.all()
        avg_rating = sum(e.overall_score for e in evals) / len(evals)
        contractor.rating = round(avg_rating, 2)
        contractor.save(update_fields=['rating'])
        
        log_audit_event(
            action='UPDATE',
            module='contractors',
            object_id=str(eval_record.id),
            object_repr=str(eval_record),
            description=f"Scorecard submitted for {contractor.company_name}. Rating: {overall:.2f}/5.00",
            user=evaluated_by
        )
        return eval_record
