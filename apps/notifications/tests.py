from django.test import TestCase
from apps.notifications.alert_router import AlertRouterEngine
from apps.notifications.escalation_ladder import EscalationLadderEngine
from apps.notifications.webhook_dispatcher import WebhookDispatcherEngine


class NotificationsEngineeringTestCase(TestCase):
    def test_alert_router(self):
        res = AlertRouterEngine.route_alert("CRITICAL", "bridges", "Scour Critical Alert")
        self.assertTrue(res["urgent_delivery"])
        self.assertIn("PAGER_SMS", res["dispatched_channels"])

    def test_escalation_ladder(self):
        res = EscalationLadderEngine.determine_current_escalation_tier(elapsed_unacknowledged_minutes=45.0)
        self.assertEqual(res["active_tier_level"], 2)

    def test_webhook_dispatcher(self):
        res = WebhookDispatcherEngine.construct_webhook_payload("ASSET_ALERT", {"id": 1}, "secret123")
        self.assertIn("X-InfraFlowX-Signature", res["headers"])
