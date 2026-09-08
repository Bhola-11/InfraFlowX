"""
InfraFlowX - Emergency Management & ICS Incident Mobilization Engine
Compliant with FEMA National Incident Management System (NIMS) Incident Command System (ICS).
"""

from typing import Dict, List, Any


class EmergencyResponseWorkflowEngine:
    """
    ICS incident activation levels and emergency resource mobilization.
    """

    ACTIVATION_LEVELS = {
        1: {"name": "LEVEL_1_FULL_ACTIVATION", "description": "Catastrophic event; multi-agency unified command"},
        2: {"name": "LEVEL_2_PARTIAL_ACTIVATION", "description": "Major disaster; dedicated EOC operations"},
        3: {"name": "LEVEL_3_ENHANCED_MONITORING", "description": "Severe weather watch or localized crisis"},
        4: {"name": "LEVEL_4_NORMAL_OPERATIONS", "description": "Steady-state routine monitoring"},
    }

    @classmethod
    def assess_incident_severity(
        cls,
        casualties_count: int,
        affected_population: int,
        critical_infrastructure_impassable: bool,
        hazardous_materials_spill: bool,
    ) -> Dict[str, Any]:
        
        score = 0
        if casualties_count > 0:
            score += 4
        if affected_population > 1000:
            score += 3
        if critical_infrastructure_impassable:
            score += 3
        if hazardous_materials_spill:
            score += 4

        if score >= 7:
            level = 1
        elif score >= 4:
            level = 2
        elif score >= 2:
            level = 3
        else:
            level = 4

        info = cls.ACTIVATION_LEVELS[level]

        return {
            "incident_severity_score": score,
            "recommended_ics_activation_level": level,
            "level_name": info["name"],
            "operational_posture": info["description"],
            "state_mutual_aid_recommended": level <= 2,
        }
