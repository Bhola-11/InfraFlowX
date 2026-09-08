from django.test import TestCase
from apps.permissions.abac_evaluator import ABACEvaluatorEngine


class PermissionsEngineeringTestCase(TestCase):
    def test_abac_evaluator(self):
        res = ABACEvaluatorEngine.evaluate_access(
            user_role="TECHNICIAN",
            user_tenant_id=1,
            target_resource_tenant_id=1,
            action="VIEW"
        )
        self.assertTrue(res["access_granted"])
