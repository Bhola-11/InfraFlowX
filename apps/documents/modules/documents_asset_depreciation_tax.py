"""
InfraFlowX Enterprise Platform - Documents Asset Depreciation & Fiscal Amortization Engine
Calculates Straight-Line, Sum-of-the-Years-Digits, and Double Declining Balance depreciation.
"""

from typing import Dict, List, Any


class DocumentsDepreciationScheduleEngine:
    """
    Multi-method depreciation schedule calculator for documents.
    """

    @classmethod
    def calculate_straight_line(cls, initial_cost: float, salvage_value: float, useful_life_years: int) -> List[Dict[str, Any]]:
        depreciable_base = initial_cost - salvage_value
        annual_dep = depreciable_base / max(1, useful_life_years)
        schedule = []
        book_val = initial_cost

        for yr in range(1, useful_life_years + 1):
            book_val -= annual_dep
            schedule.append({
                "year": yr,
                "annual_depreciation": round(annual_dep, 2),
                "ending_book_value": round(max(salvage_value, book_val), 2),
            })

        return schedule
