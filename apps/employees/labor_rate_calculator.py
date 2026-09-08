"""
InfraFlowX - Fully Burdened Labor Rate & DCAA Payroll Allocation Engine
Calculates base pay, fringe benefits, overhead multiplier, and public works billable rates.
"""

from typing import Dict, Any


class LaborRateCalculatorEngine:
    """
    Computes fully burdened labor rates for municipal public works cost accounting.
    """

    @classmethod
    def calculate_burdened_rate(
        cls,
        base_hourly_rate: float,
        fringe_benefits_pct: float = 28.0,
        overhead_pct: float = 35.0,
        general_admin_pct: float = 12.0,
        overtime_hours: float = 0.0,
        standard_hours: float = 40.0,
    ) -> Dict[str, Any]:
        
        fringe = base_hourly_rate * (fringe_benefits_pct / 100.0)
        direct_labor_burdened = base_hourly_rate + fringe
        overhead = direct_labor_burdened * (overhead_pct / 100.0)
        ga = (direct_labor_burdened + overhead) * (general_admin_pct / 100.0)
        
        fully_burdened_hourly = direct_labor_burdened + overhead + ga
        
        total_std_cost = standard_hours * fully_burdened_hourly
        total_ot_cost = overtime_hours * (fully_burdened_hourly * 1.5)
        total_payroll_cost = total_std_cost + total_ot_cost

        return {
            "base_hourly_rate": round(base_hourly_rate, 2),
            "fully_burdened_hourly_rate": round(fully_burdened_hourly, 2),
            "burden_multiplier": round(fully_burdened_hourly / base_hourly_rate, 3),
            "total_standard_cost": round(total_std_cost, 2),
            "total_overtime_cost": round(total_ot_cost, 2),
            "total_labor_cost": round(total_payroll_cost, 2),
        }
