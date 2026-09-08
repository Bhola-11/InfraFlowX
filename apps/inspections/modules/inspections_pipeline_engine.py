"""
InfraFlowX Enterprise Platform - Inspections Operations Pipeline & Decision Matrix
Automates field dispatch prioritization, resource matching, and workflow step execution.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import heapq


class InspectionsDecisionMatrixEngine:
    """
    Multi-criteria decision analysis (MCDA) and operational priority ranking for inspections.
    """

    @classmethod
    def prioritize_work_items(cls, items: List[Dict[str, Any]], max_items_to_return: int = 10) -> List[Dict[str, Any]]:
        """
        Ranks items based on Weighted Priority Score (WPS):
        WPS = 0.40 * Severity + 0.30 * Criticality + 0.20 * Backlog_Age + 0.10 * Cost_Efficiency
        """
        scored_items = []
        for item in items:
            sev = item.get("severity_score", 50.0)
            crit = item.get("criticality_score", 50.0)
            age_days = item.get("age_in_backlog_days", 10.0)
            age_score = min(100.0, age_days * 2.0)
            cost_eff = item.get("cost_efficiency_score", 50.0)

            wps = 0.40 * sev + 0.30 * crit + 0.20 * age_score + 0.10 * cost_eff
            item_with_score = {**item, "weighted_priority_score": round(wps, 2)}
            scored_items.append(item_with_score)

        scored_items.sort(key=lambda x: x["weighted_priority_score"], reverse=True)
        return scored_items[:max_items_to_return]

    @classmethod
    def allocate_personnel_skills(cls, task_requirements: List[str], available_workers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Matches skill sets between required technical qualifications and available field crews.
        """
        req_set = set(r.upper() for r in task_requirements)
        best_match = None
        best_match_count = -1

        for worker in available_workers:
            w_skills = set(s.upper() for s in worker.get("skills", []))
            common = len(req_set.intersection(w_skills))
            if common > best_match_count:
                best_match_count = common
                best_match = worker

        coverage_pct = (best_match_count / len(req_set) * 100.0) if req_set else 100.0

        return {
            "task_requirements": list(req_set),
            "selected_worker": best_match,
            "skills_matched_count": best_match_count,
            "skills_coverage_percentage": round(coverage_pct, 1),
            "fully_qualified": coverage_pct >= 100.0,
        }
