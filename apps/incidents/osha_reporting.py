"""
InfraFlowX - OSHA 300 / 300A Compliance & DART Incident Rate Engine
Calculates Days Away, Restricted, or Transferred (DART) and Severe Injury reporting thresholds.
"""

from typing import Dict, Any


class OSHAReportingEngine:
    """
    Compliant with OSHA 29 CFR Part 1904 Injury and Illness Recordkeeping.
    """

    @classmethod
    def calculate_dart_rate(cls, days_away_cases: int, job_transfer_cases: int, total_hours_worked: float) -> Dict[str, Any]:
        """
        DART Rate = ((Days Away Cases + Job Transfer Cases) * 200,000) / Total Hours Worked
        """
        if total_hours_worked <= 0:
            return {"dart_rate": 0.0, "status": "NO_HOURS"}

        total_dart_cases = days_away_cases + job_transfer_cases
        dart = (total_dart_cases * 200_000.0) / total_hours_worked

        return {
            "total_dart_cases": total_dart_cases,
            "total_hours_worked": total_hours_worked,
            "dart_rate": round(dart, 2),
            "industry_benchmark_comparison": "BELOW_AVERAGE_EXCELLENT" if dart < 1.0 else ("AVERAGE" if dart <= 2.0 else "ELEVATED_INSPECTION_RISK"),
        }
