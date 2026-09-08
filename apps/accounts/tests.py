from django.test import TestCase
from apps.accounts.password_policy import PasswordPolicyEngine


class AccountsEngineeringTestCase(TestCase):
    def test_password_strength(self):
        res = PasswordPolicyEngine.evaluate_password_strength("InfraFlowX@2026_Secure!")
        self.assertTrue(res["nist_compliant"])
