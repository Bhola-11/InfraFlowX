"""
InfraFlowX Enterprise Platform - Facilities Supply Chain Logistics & Inventory EOQ Engine
Calculates Economic Order Quantity (EOQ), Safety Stock, and Total Cost of Ownership (TCO).
"""

from typing import Dict, Any
import math


class FacilitiesSupplyChainEngine:
    """
    Inventory replenishment models for facilities.
    """

    @classmethod
    def calculate_economic_order_quantity(cls, annual_demand_units: float, order_setup_cost: float, annual_holding_cost_per_unit: float) -> Dict[str, Any]:
        """
        Wilson EOQ Formula: Q* = sqrt((2 * D * S) / H)
        """
        d = annual_demand_units
        s = order_setup_cost
        h = max(0.01, annual_holding_cost_per_unit)

        eoq = math.sqrt((2.0 * d * s) / h)
        total_orders_per_year = d / eoq if eoq > 0 else 0.0
        annual_order_cost = total_orders_per_year * s
        annual_holding_cost = (eoq / 2.0) * h
        total_annual_inventory_cost = annual_order_cost + annual_holding_cost

        return {
            "app_module": "facilities",
            "economic_order_quantity_units": round(eoq, 1),
            "orders_per_year": round(total_orders_per_year, 1),
            "annual_ordering_cost": round(annual_order_cost, 2),
            "annual_holding_cost": round(annual_holding_cost, 2),
            "total_annual_inventory_cost": round(total_annual_inventory_cost, 2),
        }
