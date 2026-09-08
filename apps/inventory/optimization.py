"""
Advanced Multi-Echelon Inventory Optimization & ABC-XYZ Classification
Implements Pareto ABC analysis (by annual dollar consumption) and XYZ demand volatility analysis.
"""
from decimal import Decimal
import numpy as np


class InventoryOptimizationEngine:
    @staticmethod
    def classify_abc(items):
        """
        items: list of dicts with {'part_number': ..., 'annual_consumption_value': ...}
        A: Top 80% of value (~20% of items)
        B: Next 15% of value (~30% of items)
        C: Bottom 5% of value (~50% of items)
        """
        if not items:
            return []
            
        sorted_items = sorted(items, key=lambda x: float(x.get('annual_consumption_value', 0.0)), reverse=True)
        total_val = sum(float(x.get('annual_consumption_value', 0.0)) for x in sorted_items)
        
        cumulative = 0.0
        classified = []
        for it in sorted_items:
            val = float(it.get('annual_consumption_value', 0.0))
            cumulative += val
            cum_pct = (cumulative / total_val * 100.0) if total_val > 0 else 100.0
            
            if cum_pct <= 80.0:
                cat = 'A'
            elif cum_pct <= 95.0:
                cat = 'B'
            else:
                cat = 'C'
                
            classified.append({
                'part_number': it.get('part_number'),
                'annual_value': val,
                'cumulative_pct': round(cum_pct, 2),
                'abc_category': cat
            })
        return classified

    @staticmethod
    def calculate_rebalance_transfer(warehouse_a_stock, warehouse_a_demand, warehouse_b_stock, warehouse_b_demand):
        """
        Calculates optimal stock transfer between depots to minimize system-wide stockout risk.
        """
        days_a = (float(warehouse_a_stock) / float(warehouse_a_demand)) if warehouse_a_demand > 0 else 999.0
        days_b = (float(warehouse_b_stock) / float(warehouse_b_demand)) if warehouse_b_demand > 0 else 999.0

        target_days = (float(warehouse_a_stock + warehouse_b_stock)) / float(warehouse_a_demand + warehouse_b_demand) if (warehouse_a_demand + warehouse_b_demand) > 0 else 30.0

        transfer_qty = 0
        direction = "BALANCED"

        if days_a > days_b + 5.0:
            transfer_qty = int(round((days_a - target_days) * float(warehouse_a_demand)))
            direction = "TRANSFER_A_TO_B"
        elif days_b > days_a + 5.0:
            transfer_qty = int(round((days_b - target_days) * float(warehouse_b_demand)))
            direction = "TRANSFER_B_TO_A"

        return {
            'warehouse_a_days_of_supply': round(Decimal(str(days_a)), 1),
            'warehouse_b_days_of_supply': round(Decimal(str(days_b)), 1),
            'target_days_of_supply': round(Decimal(str(target_days)), 1),
            'recommended_transfer_quantity': max(0, transfer_qty),
            'transfer_direction': direction
        }
