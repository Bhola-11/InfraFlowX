"""
InfraFlowX - Dynamic Inspection Checklist & Quality Assurance Scoring Engine
Compiles field inspection scoring, defect categorization, and mandatory photo verification.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class InspectionItemResponse:
    item_id: str
    category: str
    score: int  # 1 to 5 (5 = Excellent, 1 = Severe Failure)
    weight: float = 1.0
    defect_noted: bool = False
    photo_attached: bool = False
    mandatory_photo_required: bool = False
    comments: str = ""


class InspectionChecklistEngine:
    """
    Evaluates inspection responses and calculates weighted compliance index and risk flags.
    """

    @classmethod
    def score_inspection(cls, responses: List[InspectionItemResponse]) -> Dict[str, Any]:
        if not responses:
            return {"overall_score": 100.0, "status": "NO_ITEMS"}

        total_weighted_points = 0.0
        max_possible_points = 0.0
        missing_mandatory_photos = 0
        critical_defects = 0
        category_breakdown = {}

        for item in responses:
            cat = item.category
            if cat not in category_breakdown:
                category_breakdown[cat] = {"weighted_score": 0.0, "max_score": 0.0, "items_count": 0}

            points = item.score * item.weight
            max_points = 5.0 * item.weight
            
            total_weighted_points += points
            max_possible_points += max_points
            
            category_breakdown[cat]["weighted_score"] += points
            category_breakdown[cat]["max_score"] += max_points
            category_breakdown[cat]["items_count"] += 1

            if item.score <= 2 or item.defect_noted:
                critical_defects += 1

            if item.mandatory_photo_required and not item.photo_attached:
                missing_mandatory_photos += 1

        overall_pct = (total_weighted_points / max_possible_points * 100.0) if max_possible_points > 0 else 100.0

        # Calculate category scores
        categories_summary = {}
        for cat, data in category_breakdown.items():
            cat_pct = (data["weighted_score"] / data["max_score"] * 100.0) if data["max_score"] > 0 else 100.0
            categories_summary[cat] = round(cat_pct, 1)

        # Determine overall grade
        if overall_pct >= 90.0 and critical_defects == 0:
            grade = "PASSED_SUPERIOR"
        elif overall_pct >= 75.0 and critical_defects <= 1:
            grade = "PASSED_SATISFACTORY"
        elif overall_pct >= 60.0:
            grade = "CONDITIONAL_PASS_REPAIRS_REQUIRED"
        else:
            grade = "FAILED_CRITICAL_DEFICIENCIES"

        return {
            "overall_score_percentage": round(overall_pct, 1),
            "inspection_grade": grade,
            "total_items_evaluated": len(responses),
            "critical_defects_count": critical_defects,
            "missing_mandatory_photos": missing_mandatory_photos,
            "qa_compliance_passed": (missing_mandatory_photos == 0),
            "category_scores": categories_summary,
        }
