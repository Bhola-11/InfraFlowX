"""
InfraFlowX - 24/7 DuPont & Pitman 12-Hour Shift Rotation Engine
Generates continuous operations shift schedules and evaluates circadian fatigue risk.
"""

from typing import Dict, List, Any


class ShiftRotationEngine:
    """
    24/7 continuous operations shift rotation generator.
    """

    DUPONT_28_DAY_CYCLE = [
        "D", "D", "D", "D", "O", "O", "O", "O", "N", "N", "N", "O", "O", "O",
        "D", "D", "D", "O", "O", "O", "O", "N", "N", "N", "N", "O", "O", "O"
    ]

    @classmethod
    def generate_dupont_schedule(cls, team_letter: str, cycle_offset_days: int = 0) -> List[Dict[str, Any]]:
        """
        Generates 28-day DuPont shift schedule: D=Day (12h), N=Night (12h), O=Off.
        """
        schedule = []
        for day in range(28):
            idx = (day + cycle_offset_days) % 28
            shift = cls.DUPONT_28_DAY_CYCLE[idx]
            schedule.append({
                "day_number": day + 1,
                "team": team_letter,
                "shift_code": shift,
                "shift_description": "Day Shift (07:00-19:00)" if shift == "D" else ("Night Shift (19:00-07:00)" if shift == "N" else "Off Duty"),
                "hours_scheduled": 12 if shift in ("D", "N") else 0,
            })
        return schedule
