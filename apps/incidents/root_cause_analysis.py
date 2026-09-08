"""
InfraFlowX - Incident Root Cause Analysis (RCA) & Ishikawa Fishbone Engine
Decomposes infrastructure failures into 5-Whys causal chains and 6M categories.
"""

from typing import Dict, List, Any


class RootCauseAnalysisEngine:
    """
    Ishikawa diagram decomposition and corrective action tracking.
    """

    ISHIKAWA_CATEGORIES = [
        "MACHINE_EQUIPMENT",
        "METHOD_PROCEDURE",
        "MATERIAL_COMPONENT",
        "MANPOWER_HUMAN_FACTOR",
        "MEASUREMENT_INSPECTION",
        "MOTHER_NATURE_ENVIRONMENT",
    ]

    @classmethod
    def compile_rca_report(
        cls,
        incident_id: str,
        primary_failure: str,
        five_whys: List[str],
        contributing_factors: List[Dict[str, str]],  # [{"category": "MATERIAL_COMPONENT", "factor": "Corrosion in joint"}]
    ) -> Dict[str, Any]:
        
        categorized = {cat: [] for cat in cls.ISHIKAWA_CATEGORIES}
        for item in contributing_factors:
            cat = item.get("category", "METHOD_PROCEDURE").upper()
            if cat in categorized:
                categorized[cat].append(item.get("factor", ""))

        root_cause = five_whys[-1] if five_whys else primary_failure

        return {
            "incident_id": incident_id,
            "primary_failure_event": primary_failure,
            "root_cause_determination": root_cause,
            "five_whys_depth": len(five_whys),
            "five_whys_sequence": five_whys,
            "ishikawa_fishbone_breakdown": categorized,
        }
