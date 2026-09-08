"""
Support Serializers
"""
from apps.support.models import SupportTicket, TicketComment


class SupportTicketSerializer:
    @staticmethod
    def to_dict(ticket):
        return {
            'id': str(ticket.id),
            'ticket_number': ticket.ticket_number,
            'subject': ticket.subject,
            'category': ticket.category,
            'category_display': ticket.get_category_display(),
            'priority': ticket.priority,
            'priority_display': ticket.get_priority_display(),
            'status': ticket.status,
            'status_display': ticket.get_status_display(),
            'asset_id': ticket.asset.asset_id if ticket.asset else None,
            'reporter_name': ticket.reporter_name,
            'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
            'comments_count': ticket.comments.count(),
        }
