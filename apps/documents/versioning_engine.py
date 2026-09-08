"""
InfraFlowX - Engineering Document Versioning & SHA256 Integrity Engine
Computes semantic version increments (Major.Minor.Patch) and digital cryptographic fingerprints.
"""

from typing import Dict, Any
import hashlib


class DocumentVersioningEngine:
    """
    Manages document version lifecycles and cryptographic checksum validation.
    """

    @classmethod
    def calculate_sha256_fingerprint(cls, content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    @classmethod
    def compute_next_version(cls, current_version: str, change_type: str = "MINOR") -> str:
        """
        change_type: MAJOR, MINOR, PATCH
        """
        parts = current_version.strip().lstrip("v").split(".")
        try:
            major = int(parts[0])
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
        except (ValueError, IndexError):
            major, minor, patch = 1, 0, 0

        c_type = change_type.upper()
        if c_type == "MAJOR":
            major += 1
            minor = 0
            patch = 0
        elif c_type == "MINOR":
            minor += 1
            patch = 0
        else:  # PATCH
            patch += 1

        return f"v{major}.{minor}.{patch}"
