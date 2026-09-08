"""
Supply Chain & Materials Optimization Engine
Implements Economic Order Quantity (EOQ), Safety Stock calculation, and Reorder Point automation.
"""
from decimal import Decimal
import math


class SupplyChainEngine:
    @staticmethod
    def calculate_eoq(annual_demand_units, order_cost_usd, annual_holding_cost_per_unit):
        """
        Wilson Economic Order Quantity formula:
        EOQ = sqrt((2 * D * S) / H)
        """
        d = float(annual_demand_units)
        s = float(order_cost_usd)
        h = max(0.01, float(annual_holding_cost_per_unit))
        eoq = math.sqrt((2.0 * d * s) / h)
        return int(round(eoq))

    @staticmethod
    def calculate_safety_stock(lead_time_days, daily_usage_avg, daily_usage_std_dev=2.0, service_level_z=1.65):
        """
        Safety Stock = Z * sqrt(Lead Time) * Std Dev of Daily Demand
        Reorder Point (ROP) = (Lead Time * Daily Usage) + Safety Stock
        """
        lt = float(lead_time_days)
        z = float(service_level_z)
        sigma = float(daily_usage_std_dev)
        d_avg = float(daily_usage_avg)
        
        ss = z * math.sqrt(lt) * sigma
        rop = (lt * d_avg) + ss
        return {
            'safety_stock': int(round(ss)),
            'reorder_point': int(round(rop))
        }
