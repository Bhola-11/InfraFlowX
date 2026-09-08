"""
InfraFlowX - Lotted Inventory & FIFO/LIFO/FEFO Layer Depletion Engine
Computes inventory valuations and COGS using First-In First-Out and First-Expired First-Out.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import date


@dataclass
class InventoryLot:
    lot_number: str
    quantity: float
    unit_cost: float
    received_date: date
    expiry_date: date = None


class LottedInventoryValuationEngine:
    """
    FIFO / FEFO inventory layer depletion calculator.
    """

    @classmethod
    def deplete_fifo(cls, lots: List[InventoryLot], units_demanded: float) -> Dict[str, Any]:
        sorted_lots = sorted(lots, key=lambda x: x.received_date)
        remaining_demand = units_demanded
        total_cogs = 0.0
        depleted_layers = []
        updated_lots = []

        for lot in sorted_lots:
            if remaining_demand <= 0:
                updated_lots.append(lot)
                continue

            if lot.quantity <= remaining_demand:
                take_qty = lot.quantity
                cost = take_qty * lot.unit_cost
                total_cogs += cost
                remaining_demand -= take_qty
                depleted_layers.append({"lot_number": lot.lot_number, "depleted_qty": take_qty, "unit_cost": lot.unit_cost, "layer_cogs": cost})
            else:
                take_qty = remaining_demand
                cost = take_qty * lot.unit_cost
                total_cogs += cost
                remaining_qty = lot.quantity - take_qty
                updated_lots.append(InventoryLot(lot.lot_number, remaining_qty, lot.unit_cost, lot.received_date, lot.expiry_date))
                depleted_layers.append({"lot_number": lot.lot_number, "depleted_qty": take_qty, "unit_cost": lot.unit_cost, "layer_cogs": cost})
                remaining_demand = 0.0

        return {
            "units_demanded": units_demanded,
            "units_fulfilled": units_demanded - remaining_demand,
            "total_cogs": round(total_cogs, 2),
            "depleted_layers": depleted_layers,
            "unfulfilled_units": max(0.0, remaining_demand),
        }
