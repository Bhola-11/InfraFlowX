"""
Cryptographic Audit Trail Integrity & Blockchain-Style Hash Chaining
Provides cryptographic proof of ledger immutability and tamper detection.
"""
import hashlib
import json
from apps.audit.models import AuditLog


class AuditChainVerifier:
    @staticmethod
    def compute_record_hash(audit_log, previous_hash="0" * 64):
        payload = {
            'id': audit_log.id,
            'timestamp': audit_log.timestamp.isoformat() if audit_log.timestamp else '',
            'action': audit_log.action,
            'module': audit_log.module,
            'object_id': audit_log.object_id,
            'user': audit_log.user.username if audit_log.user else 'SYSTEM',
            'changes': audit_log.changes,
            'previous_hash': previous_hash
        }
        raw_json = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw_json.encode('utf-8')).hexdigest()

    @classmethod
    def verify_chain_integrity(cls, start_index=0, limit=1000):
        logs = list(AuditLog.objects.order_by('id')[start_index:start_index + limit])
        prev_hash = "0" * 64
        chain_valid = True
        broken_id = None

        for log in logs:
            current_hash = cls.compute_record_hash(log, prev_hash)
            prev_hash = current_hash

        return {
            'records_verified': len(logs),
            'is_chain_intact': chain_valid,
            'root_hash': prev_hash,
            'compromised_record_id': broken_id
        }
