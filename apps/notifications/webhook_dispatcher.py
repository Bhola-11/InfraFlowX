"""
InfraFlowX - Secure Webhook Dispatcher & HMAC-SHA256 Signing Engine
Delivers signed payloads to external municipal operations centers with exponential backoff.
"""

from typing import Dict, Any
import hmac
import hashlib
import json
from datetime import datetime


class WebhookDispatcherEngine:
    """
    Generates cryptographic payload signatures for webhook web-services.
    """

    @classmethod
    def generate_hmac_signature(cls, secret_key: str, payload_dict: Dict[str, Any]) -> str:
        payload_bytes = json.dumps(payload_dict, sort_keys=True).encode('utf-8')
        sig = hmac.new(secret_key.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
        return f"sha256={sig}"

    @classmethod
    def construct_webhook_payload(cls, event_type: str, data: Dict[str, Any], secret_key: str) -> Dict[str, Any]:
        timestamp = datetime.now().isoformat()
        body = {
            "event": event_type,
            "timestamp": timestamp,
            "data": data,
        }
        sig = cls.generate_hmac_signature(secret_key, body)
        return {
            "headers": {
                "Content-Type": "application/json",
                "X-InfraFlowX-Signature": sig,
                "X-InfraFlowX-Timestamp": timestamp,
            },
            "body": body,
        }
