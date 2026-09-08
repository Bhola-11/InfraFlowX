"""
InfraFlowX - Parametric Work Order Unit Cost Estimation Engine
Calculates standard labor, heavy equipment, materials, and municipal overhead loadings.
"""

from typing import Dict, List, Any


class WorkOrderCostEstimator:
    """
    Parametric RSMeans-style work order budgeting and estimation.
    """

    @classmethod
    def estimate_work_order_cost(
        cls,
        labor_items: List[Dict[str, float]],       # [{"hours": 10.0, "hourly_rate": 55.0}]
        equipment_items: List[Dict[str, float]],   # [{"hours": 8.0, "rental_rate_hr": 120.0}]
        material_items: List[Dict[str, float]],    # [{"quantity": 5.0, "unit_cost": 250.0}]
        overhead_markup_pct: float = 15.0,
        contingency_pct: float = 10.0,
    ) -> Dict[str, Any]:
        
        direct_labor = sum(item.get("hours", 0.0) * item.get("hourly_rate", 0.0) for item in labor_items)
        direct_equipment = sum(item.get("hours", 0.0) * item.get("rental_rate_hr", 0.0) for item in equipment_items)
        direct_materials = sum(item.get("quantity", 0.0) * item.get("unit_cost", 0.0) for item in material_items)

        subtotal_direct = direct_labor + direct_equipment + direct_materials
        overhead_amount = subtotal_direct * (overhead_markup_pct / 100.0)
        subtotal_with_overhead = subtotal_direct + overhead_amount
        contingency_amount = subtotal_with_overhead * (contingency_pct / 100.0)
        
        grand_total = subtotal_with_overhead + contingency_amount

        return {
            "direct_labor_cost": round(direct_labor, 2),
            "direct_equipment_cost": round(direct_equipment, 2),
            "direct_materials_cost": round(direct_materials, 2),
            "subtotal_direct_costs": round(subtotal_direct, 2),
            "overhead_cost": round(overhead_amount, 2),
            "contingency_cost": round(contingency_amount, 2),
            "grand_total_estimated_cost": round(grand_total, 2),
        }
