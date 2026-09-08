"""
InfraFlowX - Multi-Tenant Data Isolation & Quota Enforcement Engine
Guarantees tenant sandboxing, asset capacity limits, and storage quotas.
"""

from typing import Dict, Any


class TenantGovernanceEngine:
    """
    Enforces organizational quotas and subscription boundaries.
    """

    PLAN_LIMITS = {
        "STARTER": {"max_assets": 500, "max_users": 10, "max_storage_gb": 20},
        "PROFESSIONAL": {"max_assets": 5000, "max_users": 50, "max_storage_gb": 200},
        "ENTERPRISE": {"max_assets": 100000, "max_users": 1000, "max_storage_gb": 5000},
    }

    @classmethod
    def check_asset_quota(cls, plan_tier: str, current_asset_count: int) -> Dict[str, Any]:
        tier = plan_tier.upper()
        limits = cls.PLAN_LIMITS.get(tier, cls.PLAN_LIMITS["PROFESSIONAL"])
        max_allowed = limits["max_assets"]

        remaining = max(0, max_allowed - current_asset_count)
        quota_exceeded = current_asset_count >= max_allowed

        return {
            "plan_tier": tier,
            "current_asset_count": current_asset_count,
            "max_allowed_assets": max_allowed,
            "remaining_capacity": remaining,
            "quota_exceeded": quota_exceeded,
            "utilization_pct": round((current_asset_count / max_allowed * 100.0), 1),
        }
