"""
InfraFlowX - Finite State Machine & Business Process Workflow Engine for Assets
Enforces deterministic status transitions, pre-condition checks, and role authorization.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger("infraflowx.assets.workflow")


class AssetsWorkflowStateMachine:
    """
    Deterministic Finite State Machine (FSM) controlling assets entity lifecycles.
    """

    STATE_TRANSITIONS: Dict[str, List[str]] = {
        "DRAFT": ["PENDING_REVIEW", "CANCELLED"],
        "PENDING_REVIEW": ["APPROVED", "REJECTED", "REVISION_REQUESTED"],
        "REVISION_REQUESTED": ["PENDING_REVIEW", "CANCELLED"],
        "APPROVED": ["IN_PROGRESS", "ACTIVE", "SCHEDULED", "SUSPENDED"],
        "IN_PROGRESS": ["COMPLETED", "ON_HOLD", "CANCELLED"],
        "ON_HOLD": ["IN_PROGRESS", "CANCELLED"],
        "COMPLETED": ["CLOSED", "VERIFIED", "ARCHIVED"],
        "CLOSED": ["ARCHIVED"],
        "REJECTED": ["DRAFT", "CANCELLED"],
        "CANCELLED": ["ARCHIVED"],
        "ARCHIVED": [],
    }

    @classmethod
    def is_transition_permitted(cls, current_state: str, target_state: str) -> bool:
        curr = current_state.upper()
        target = target_state.upper()
        allowed = cls.STATE_TRANSITIONS.get(curr, [])
        return target in allowed

    @classmethod
    def execute_transition(
        cls,
        entity_id: int,
        current_state: str,
        target_state: str,
        user_role: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        
        curr = current_state.upper()
        target = target_state.upper()

        if not cls.is_transition_permitted(curr, target):
            logger.warning(f"Invalid state transition attempted for assets #{entity_id}: {curr} -> {target}")
            return {
                "success": False,
                "error": f"Transition from {curr} to {target} is not permitted.",
                "current_state": curr,
            }

        # Role-based validation
        if target in ("APPROVED", "CLOSED") and user_role not in ("ADMIN", "DIRECTOR", "MANAGER", "SUPERVISOR", "ENGINEER"):
            return {
                "success": False,
                "error": f"Role {user_role} lacks authorization to transition entity to {target}.",
                "current_state": curr,
            }

        logger.info(f"State transition executed for assets #{entity_id}: {curr} -> {target} by {user_role}")
        
        return {
            "success": True,
            "entity_id": entity_id,
            "previous_state": curr,
            "new_state": target,
            "timestamp": datetime.now().isoformat(),
            "authorized_by_role": user_role,
            "transition_reason": reason or "Standard workflow progression",
        }
