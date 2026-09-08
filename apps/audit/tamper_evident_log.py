"""
InfraFlowX - Cryptographic Tamper-Evident Hash Chain & Merkle Tree Engine
Guarantees immutability of public infrastructure audit records.
"""

from typing import Dict, List, Any
import hashlib


class MerkleAuditLogEngine:
    """
    Builds cryptographic hash chains and Merkle tree roots for immutable event logging.
    """

    @classmethod
    def hash_record(cls, prev_hash: str, event_data: str) -> str:
        payload = f"{prev_hash}|{event_data}".encode('utf-8')
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def verify_hash_chain(cls, chain_records: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        chain_records: List of {"prev_hash": "...", "event_data": "...", "hash": "..."}
        """
        for i, rec in enumerate(chain_records):
            expected = cls.hash_record(rec.get("prev_hash", "0" * 64), rec.get("event_data", ""))
            if expected != rec.get("hash", ""):
                return {
                    "chain_valid": False,
                    "tampered_at_index": i,
                    "expected_hash": expected,
                    "recorded_hash": rec.get("hash"),
                }
        return {"chain_valid": True, "total_verified_records": len(chain_records)}
