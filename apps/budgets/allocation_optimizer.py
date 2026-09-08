"""
InfraFlowX - Knapsack Capital Budget Optimization Engine
Maximizes infrastructure condition improvement across competing capital projects under budget constraints.
"""

from typing import Dict, List, Any


class BudgetAllocationOptimizer:
    """
    0/1 Knapsack dynamic programming optimization for public capital programs.
    """

    @classmethod
    def optimize_capital_allocation(
        cls,
        available_budget: float,
        candidate_projects: List[Dict[str, Any]],  # [{"id": 1, "name": "...", "cost": 500000.0, "benefit_score": 85.0}]
    ) -> Dict[str, Any]:
        """
        Dynamic programming 0/1 knapsack implementation.
        Scales budget to discrete integer units for exact solution.
        """
        if not candidate_projects or available_budget <= 0:
            return {"allocated_projects": [], "total_cost": 0.0, "total_benefit": 0.0}

        # Scale costs to integer thousands
        scale = 1000.0
        int_budget = int(available_budget / scale)
        n = len(candidate_projects)

        dp = [[0.0] * (int_budget + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            p = candidate_projects[i - 1]
            p_cost = max(1, int(p.get("cost", 0.0) / scale))
            p_benefit = p.get("benefit_score", 0.0)

            for w in range(int_budget + 1):
                if p_cost <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - p_cost] + p_benefit)
                else:
                    dp[i][w] = dp[i - 1][w]

        # Backtrack to find chosen projects
        selected_projects = []
        w = int_budget
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                p = candidate_projects[i - 1]
                selected_projects.append(p)
                p_cost = max(1, int(p.get("cost", 0.0) / scale))
                w -= p_cost

        total_cost = sum(p["cost"] for p in selected_projects)
        total_benefit = sum(p.get("benefit_score", 0.0) for p in selected_projects)

        return {
            "selected_projects_count": len(selected_projects),
            "allocated_projects": selected_projects,
            "total_allocated_cost": round(total_cost, 2),
            "remaining_unallocated_budget": round(available_budget - total_cost, 2),
            "total_benefit_score": round(total_benefit, 2),
            "budget_utilization_pct": round((total_cost / available_budget * 100.0) if available_budget > 0 else 0.0, 2),
        }
