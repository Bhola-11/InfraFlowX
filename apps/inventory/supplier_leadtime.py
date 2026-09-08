"""
InfraFlowX - Supplier Lead Time & On-Time Delivery (OTD) Performance Engine
Calculates lead time standard deviation, supplier reliability score, and stockout buffer days.
"""

from typing import Dict, List, Any
import math


class SupplierLeadTimeEngine:
    """
    Evaluates vendor delivery variability and safety stock buffers.
    """

    @classmethod
    def analyze_supplier_performance(cls, delivery_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        delivery_records: List of {"promised_days": 14, "actual_days": 16, "on_time": False}
        """
        if not delivery_records:
            return {"status": "NO_RECORDS"}

        actual_days = [r["actual_days"] for r in delivery_records]
        mean_lead = sum(actual_days) / len(actual_days)
        variance = sum((x - mean_lead) ** 2 for x in actual_days) / len(actual_days) if len(actual_days) > 1 else 0.0
        std_lead = math.sqrt(variance)

        on_time_count = sum(1 for r in delivery_records if r.get("on_time", False) or r["actual_days"] <= r["promised_days"])
        otd_pct = (on_time_count / len(delivery_records)) * 100.0

        # Recommended safety buffer days (Z=1.65 for 95% service level)
        buffer_days = math.ceil(1.65 * std_lead)

        return {
            "total_shipments_evaluated": len(delivery_records),
            "mean_lead_time_days": round(mean_lead, 1),
            "lead_time_std_dev_days": round(std_lead, 2),
            "on_time_delivery_pct": round(otd_pct, 1),
            "recommended_safety_buffer_days": buffer_days,
            "vendor_grade": "TIER_1_PREFERRED" if otd_pct >= 95.0 else ("TIER_2_QUALIFIED" if otd_pct >= 85.0 else "TIER_3_PROBATION"),
        }
