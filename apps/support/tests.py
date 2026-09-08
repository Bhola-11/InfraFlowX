"""
Comprehensive Unit Tests for Support App
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.support.models import SupportTicket, TicketComment, SLAPolicy
from apps.support.services import SupportService

User = get_user_model()


class SupportTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='support_agent', password='password123')
        self.policy = SLAPolicy.objects.create(
            name='High Priority Hazard SLA',
            priority='HIGH',
            response_time_hours=6,
            resolution_time_hours=24
        )
        self.ticket = SupportTicket.objects.create(
            ticket_number='TKT-TEST-01',
            subject='Hazardous pothole on expressway exit',
            category='POTHOLE_HAZARD',
            priority='HIGH',
            status='NEW',
            reporter_name='Citizen Jane Doe',
            description='Deep pothole damaging vehicles'
        )

    def test_sla_evaluation(self):
        sla = SupportService.evaluate_ticket_sla_status(self.ticket)
        self.assertEqual(sla['target_hours'], 24)
        self.assertFalse(sla['is_breached'])

    def test_add_comment(self):
        comment = SupportService.add_ticket_comment(
            ticket_id=self.ticket.id,
            comment_text='Dispatched field crew WO-0491 to site.',
            author=self.user
        )
        self.assertEqual(comment.ticket, self.ticket)
