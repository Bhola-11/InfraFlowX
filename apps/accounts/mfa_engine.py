"""
InfraFlowX - Multi-Factor Authentication (MFA) & TOTP RFC 6238 Engine
Generates and validates time-based one-time passwords for administrative accounts.
"""

from typing import Dict, Any
import hashlib
import hmac
import time
import struct
import base64


class TOTPAuthenticationEngine:
    """
    RFC 6238 Time-Based One-Time Password algorithm.
    """

    @classmethod
    def generate_totp_code(cls, secret_key: str, time_step_seconds: int = 30, digits: int = 6) -> str:
        key = base64.b32decode(secret_key.upper(), casefold=True)
        counter = int(time.time() // time_step_seconds)
        msg = struct.pack(">Q", counter)
        
        h = hmac.new(key, msg, hashlib.sha1).digest()
        offset = h[-1] & 0x0F
        binary = ((h[offset] & 0x7F) << 24) | ((h[offset + 1] & 0xFF) << 16) | ((h[offset + 2] & 0xFF) << 8) | (h[offset + 3] & 0xFF)
        otp = binary % (10 ** digits)
        return str(otp).zfill(digits)

    @classmethod
    def verify_totp(cls, entered_code: str, secret_key: str, tolerance_steps: int = 1) -> bool:
        try:
            key = base64.b32decode(secret_key.upper(), casefold=True)
        except Exception:
            return False

        current_counter = int(time.time() // 30)
        for offset in range(-tolerance_steps, tolerance_steps + 1):
            counter = current_counter + offset
            msg = struct.pack(">Q", counter)
            h = hmac.new(key, msg, hashlib.sha1).digest()
            o = h[-1] & 0x0F
            binary = ((h[o] & 0x7F) << 24) | ((h[o + 1] & 0xFF) << 16) | ((h[o + 2] & 0xFF) << 8) | (h[o + 3] & 0xFF)
            otp = str(binary % (10 ** 6)).zfill(6)
            if otp == entered_code.strip():
                return True
        return False
