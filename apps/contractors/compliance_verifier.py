"""
InfraFlowX - Contractor Compliance & Safety Performance Index Engine
Evaluates OSHA Recordable Incident Rate (TRIR), Experience Modification Rate (EMR), and insurance.
"""

from typing import Dict, Any
from datetime import date


class ContractorComplianceEngine:
    """
    Safety qualifications and municipal regulatory verification.
    """

    @classmethod
    def calculate_osha_trir(cls, num_recordable_injuries: int, total_hours_worked: float) -> Dict[str, Any]:
        """
        Total Recordable Incident Rate (TRIR) = (Injuries * 200,000) / Total Hours Worked
        """
        if total_hours_worked <= 0:
            return {"trir": 0.0, "status": "NO_HOURS"}

        trir = (num_recordable_injuries * 200_000.0) / total_hours_worked
        
        # Benchmark comparison: US Construction Industry Average is ~2.5
        safety_status = "EXCELLENT" if trir < 1.5 else ("ACCEPTABLE" if trir <= 3.0 else "POOR_SAFETY_AUDIT_REQUIRED")

        return {
            "total_recordable_injuries": num_recordable_injuries,
            "total_hours_worked": total_hours_worked,
            "calculated_trir": round(trir, 2),
            "safety_rating": safety_status,
            "qualification_passed": trir <= 3.0,
        }

    @classmethod
    def verify_insurance_coverage(
        cls,
        general_liability_active: bool,
        general_liability_limit: float,
        workers_comp_active: bool,
        certificate_expiry: date,
        current_date: date,
        min_required_liability: float = 2_000_000.0,
    ) -> Dict[str, Any]:
        
        expired = certificate_expiry < current_date
        days_to_expiration = (certificate_expiry - current_date).days
        sufficient_limit = general_liability_limit >= min_required_liability
        
        passed = general_liability_active and workers_comp_active and (not expired) and sufficient_limit

        return {
            "insurance_verified": passed,
            "certificate_expired": expired,
            "days_until_expiration": days_to_expiration,
            "liability_coverage_adequate": sufficient_limit,
            "workers_compensation_verified": workers_comp_active,
            "warning_flag": days_to_expiration <= 30 and not expired,
        }
