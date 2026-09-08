from django.test import TestCase
from apps.audit.tamper_evident_log import MerkleAuditLogEngine
from apps.audit.compliance_reporter import ComplianceReporterEngine


class AuditEngineeringTestCase(TestCase):
    def test_merkle_audit_chain(self):
        h0 = "0" * 64
        h1 = MerkleAuditLogEngine.hash_record(h0, "Event 1")
        h2 = MerkleAuditLogEngine.hash_record(h1, "Event 2")
        chain = [
            {"prev_hash": h0, "event_data": "Event 1", "hash": h1},
            {"prev_hash": h1, "event_data": "Event 2", "hash": h2},
        ]
        res = MerkleAuditLogEngine.verify_hash_chain(chain)
        self.assertTrue(res["chain_valid"])

    def test_soc2_compliance_report(self):
        events = [{"action_type": "ROLE_CHANGE", "is_violation": False}]
        res = ComplianceReporterEngine.generate_soc2_evidence_package(events)
        self.assertEqual(res["compliance_status"], "FULL_COMPLIANCE_PASSED")
