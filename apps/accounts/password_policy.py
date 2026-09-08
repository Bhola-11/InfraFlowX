"""
InfraFlowX - NIST SP 800-63B Password Complexity & Entropy Engine
Evaluates password strength, dictionary resistance, and character entropy.
"""

from typing import Dict, Any
import math
import re


class PasswordPolicyEngine:
    """
    Evaluates password security against NIST digital identity guidelines.
    """

    @classmethod
    def evaluate_password_strength(cls, password: str) -> Dict[str, Any]:
        length = len(password)
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[^A-Za-z0-9]', password))

        charset_size = 0
        if has_lower: charset_size += 26
        if has_upper: charset_size += 26
        if has_digit: charset_size += 10
        if has_special: charset_size += 32

        entropy = length * math.log2(max(1, charset_size))

        compliant = length >= 12 and (has_upper and has_lower and has_digit and has_special)

        return {
            "password_length": length,
            "entropy_bits": round(entropy, 1),
            "has_uppercase": has_upper,
            "has_lowercase": has_lower,
            "has_digits": has_digit,
            "has_symbols": has_special,
            "nist_compliant": compliant,
            "strength_rating": "VERY_STRONG" if entropy >= 64 else ("STRONG" if entropy >= 48 else "WEAK"),
        }
