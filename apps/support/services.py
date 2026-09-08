"""
Support & Citizen Grievance SLA Services
"""
from decimal import Decimal
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from apps.support.models import SupportTicket, TicketComment, SLAPolicy
from apps.audit.utils import log_audit_event


class SupportService:
    @staticmethod
    def evaluate_ticket_sla_status(ticket):
        policy = SLAPolicy.objects.filter(priority=ticket.priority).first()
        res_hours = policy.resolution_time_hours if policy else 72
        
        elapsed = timezone.now() - ticket.created_at
        elapsed_hours = elapsed.total_seconds() / 3600.0
        
        is_breached = (elapsed_hours > res_hours) and (ticket.status not in ['RESOLVED', 'CLOSED'])
        hours_remaining = max(0.0, res_hours - elapsed_hours)
        
        return {
            'ticket_number': ticket.ticket_number,
            'priority': ticket.priority,
            'target_hours': res_hours,
            'elapsed_hours': round(elapsed_hours, 1),
            'hours_remaining': round(hours_remaining, 1),
            'is_breached': is_breached
        }

    @staticmethod
    @transaction.atomic
    def add_ticket_comment(ticket_id, comment_text, author=None, is_internal=False):
        ticket = SupportTicket.objects.get(id=ticket_id)
        comment = TicketComment.objects.create(
            ticket=ticket,
            author=author,
            author_name=author.get_full_name() if author else "Support Team",
            comment=comment_text,
            is_internal_note=is_internal
        )
        return comment
