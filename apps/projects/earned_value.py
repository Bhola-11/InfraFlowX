"""
InfraFlowX - Earned Value Management (EVM) Project Performance Engine
Compliant with ANSI/EIA-748 Earned Value Management Systems.
"""

from typing import Dict, Any


class EarnedValueManagementEngine:
    """
    Computes PV, EV, AC, Cost Variance (CV), Schedule Variance (SV),
    Cost Performance Index (CPI), Schedule Performance Index (SPI),
    and Estimate at Completion (EAC).
    """

    @classmethod
    def calculate_evm_metrics(
        cls,
        planned_value_pv: float,
        earned_value_ev: float,
        actual_cost_ac: float,
        budget_at_completion_bac: float,
    ) -> Dict[str, Any]:
        
        cv = earned_value_ev - actual_cost_ac
        sv = earned_value_ev - planned_value_pv
        
        cpi = (earned_value_ev / actual_cost_ac) if actual_cost_ac > 0 else 1.0
        spi = (earned_value_ev / planned_value_pv) if planned_value_pv > 0 else 1.0
        
        # Estimate at Completion: EAC = BAC / CPI
        eac = (budget_at_completion_bac / cpi) if cpi > 0 else budget_at_completion_bac
        etc = max(0.0, eac - actual_cost_ac)
        vac = budget_at_completion_bac - eac
        
        # To-Complete Performance Index (TCPI) to meet BAC: (BAC - EV) / (BAC - AC)
        denom_tcpi = budget_at_completion_bac - actual_cost_ac
        tcpi = ((budget_at_completion_bac - earned_value_ev) / denom_tcpi) if denom_tcpi > 0 else 1.0

        return {
            "planned_value_pv": round(planned_value_pv, 2),
            "earned_value_ev": round(earned_value_ev, 2),
            "actual_cost_ac": round(actual_cost_ac, 2),
            "budget_at_completion_bac": round(budget_at_completion_bac, 2),
            "cost_variance_cv": round(cv, 2),
            "schedule_variance_sv": round(sv, 2),
            "cost_performance_index_cpi": round(cpi, 3),
            "schedule_performance_index_spi": round(spi, 3),
            "cost_status": "UNDER_BUDGET" if cv >= 0 else "OVER_BUDGET",
            "schedule_status": "AHEAD_OF_SCHEDULE" if sv >= 0 else "BEHIND_SCHEDULE",
            "estimate_at_completion_eac": round(eac, 2),
            "estimate_to_complete_etc": round(etc, 2),
            "variance_at_completion_vac": round(vac, 2),
            "to_complete_performance_index_tcpi": round(tcpi, 3),
        }
