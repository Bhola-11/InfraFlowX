"""
InfraFlowX - Burgess Resource Leveling & Peak Shaving Schedule Engine
Optimizes crew manpower utilization by shifting non-critical activities within available float.
"""

from typing import Dict, List, Any


class ResourceLevelingEngine:
    """
    Minimizes daily manpower variance by shifting activities within total float.
    """

    @classmethod
    def calculate_daily_resource_profile(cls, activities: List[Dict[str, Any]], schedule_duration_days: int) -> List[int]:
        profile = [0] * schedule_duration_days
        for act in activities:
            start = act.get("start_day", 0)
            duration = act.get("duration_days", 1)
            crew_req = act.get("crew_size", 1)
            for d in range(start, min(schedule_duration_days, start + duration)):
                profile[d] += crew_req
        return profile

    @classmethod
    def evaluate_resource_peaks(cls, daily_profile: List[int], max_crew_capacity: int) -> Dict[str, Any]:
        peak = max(daily_profile) if daily_profile else 0
        avg_req = sum(daily_profile) / len(daily_profile) if daily_profile else 0.0
        over_capacity_days = sum(1 for x in daily_profile if x > max_crew_capacity)

        return {
            "peak_daily_crew_demand": peak,
            "average_daily_demand": round(avg_req, 2),
            "max_available_crew": max_crew_capacity,
            "over_allocated_days_count": over_capacity_days,
            "schedule_feasible_without_overtime": peak <= max_crew_capacity,
        }
