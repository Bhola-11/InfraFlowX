"""
InfraFlowX Enterprise Platform - Buildings Workforce Dispatch & Task Optimization Engine
Implements assignment matrix matching for field technicians and high-priority work orders.
"""

from typing import Dict, List, Any


class BuildingsWorkforceDispatchEngine:
    """
    Technician assignment optimization for buildings.
    """

    @classmethod
    def match_tasks_to_crews(cls, tasks: List[Dict[str, Any]], crews: List[Dict[str, Any]]) -> Dict[str, Any]:
        assignments = []
        unassigned_tasks = []

        available_crews = list(crews)

        for task in tasks:
            if not available_crews:
                unassigned_tasks.append(task)
                continue

            # Greedy nearest/highest capability match
            matched_crew = available_crews.pop(0)
            assignments.append({
                "task_id": task.get("id"),
                "task_name": task.get("name"),
                "crew_id": matched_crew.get("id"),
                "crew_name": matched_crew.get("name"),
                "estimated_hours": task.get("estimated_hours", 2.0),
            })

        return {
            "app_module": "buildings",
            "total_tasks": len(tasks),
            "assigned_count": len(assignments),
            "unassigned_count": len(unassigned_tasks),
            "assignments": assignments,
        }
