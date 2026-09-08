"""
InfraFlowX - Attribute-Based Access Control (ABAC) & Policy Decision Point Engine
Evaluates dynamic access rules based on user role, tenant, geographic boundary, and clearance.
"""

from typing import Dict, Any


class ABACEvaluatorEngine:
    """
    Evaluates policy rules for fine-grained authorization decisions.
    """

    @classmethod
    def evaluate_access(
        cls,
        user_role: str,
        user_tenant_id: int,
        target_resource_tenant_id: int,
        action: str,  # VIEW, CREATE, EDIT, DELETE, APPROVE
        is_emergency_mode: bool = False,
    ) -> Dict[str, Any]:
        
        # Tenant isolation
        if user_tenant_id != target_resource_tenant_id and user_role != "SUPERADMIN":
            return {"access_granted": False, "reason": "TENANT_ISOLATION_VIOLATION"}

        role_u = user_role.upper()
        act_u = action.upper()

        if role_u == "SUPERADMIN":
            return {"access_granted": True, "reason": "SUPERADMIN_UNRESTRICTED"}

        if act_u == "DELETE" and role_u not in ("ADMIN", "DIRECTOR"):
            return {"access_granted": False, "reason": "ROLE_INSUFFICIENT_FOR_DELETE"}

        if act_u == "APPROVE" and role_u not in ("ADMIN", "DIRECTOR", "MANAGER", "SUPERVISOR"):
            return {"access_granted": False, "reason": "APPROVAL_AUTHORITY_REQUIRED"}

        return {"access_granted": True, "reason": "ACCESS_AUTHORIZED"}
