"""
InfraFlowX - Fixed Asset Depreciation & Tax Accounting Engine
Computes MACRS, Section 179 expensing, and straight-line municipal depreciation.
"""

from typing import Dict, List, Any


class AssetTaxDepreciationEngine:
    """
    Calculates IRS MACRS (Modified Accelerated Cost Recovery System) half-year convention schedules.
    """

    # MACRS 5-Year Property Rates (Half-Year Convention)
    MACRS_5_YEAR = [0.2000, 0.3200, 0.1920, 0.1152, 0.1152, 0.0576]
    # MACRS 7-Year Property Rates
    MACRS_7_YEAR = [0.1429, 0.2449, 0.1749, 0.1249, 0.0893, 0.0892, 0.0893, 0.0446]

    @classmethod
    def generate_macrs_schedule(cls, cost_basis: float, recovery_period_years: int = 5) -> List[Dict[str, Any]]:
        rates = cls.MACRS_5_YEAR if recovery_period_years == 5 else cls.MACRS_7_YEAR
        schedule = []
        accumulated_depreciation = 0.0
        book_value = cost_basis

        for yr, rate in enumerate(rates, start=1):
            dep_amount = cost_basis * rate
            accumulated_depreciation += dep_amount
            book_value = max(0.0, cost_basis - accumulated_depreciation)
            schedule.append({
                "year": yr,
                "recovery_rate": rate,
                "depreciation_deduction": round(dep_amount, 2),
                "accumulated_depreciation": round(accumulated_depreciation, 2),
                "ending_book_value": round(book_value, 2),
            })

        return schedule
