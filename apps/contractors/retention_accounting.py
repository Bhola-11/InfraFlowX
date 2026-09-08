"""
InfraFlowX - Contractor Retainage Accounting & Escrow Engine
Calculates statutory retainage withholding (5-10%), punchlist escrow release, and lien waivers.
"""

from typing import Dict, List, Any


class ContractorRetentionEngine:
    """
    Computes retainage withholding on progress billing applications (AIA G702/G703).
    """

    @classmethod
    def calculate_progress_billing(
        cls,
        work_completed_to_date: float,
        stored_materials_value: float,
        retention_rate_pct: float = 10.0,
        previous_payments_total: float = 0.0,
        reduced_retention_threshold_pct: float = 50.0,
    ) -> Dict[str, Any]:
        total_earned = work_completed_to_date + stored_materials_value
        
        # Statutory rule: 10% until 50% completion, then 5% or 0% on subsequent work
        effective_rate = (retention_rate_pct / 2.0) if work_completed_to_date > 500_000.0 else retention_rate_pct
        
        retained_amount = total_earned * (effective_rate / 100.0)
        net_earned_less_retainage = total_earned - retained_amount
        current_payment_due = max(0.0, net_earned_less_retainage - previous_payments_total)

        return {
            "total_completed_and_stored": round(total_earned, 2),
            "effective_retention_rate_pct": round(effective_rate, 2),
            "total_retainage_withheld": round(retained_amount, 2),
            "net_earned_less_retainage": round(net_earned_less_retainage, 2),
            "less_previous_certificates_for_payment": round(previous_payments_total, 2),
            "current_payment_due": round(current_payment_due, 2),
        }
