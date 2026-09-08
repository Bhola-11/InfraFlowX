"""
InfraFlowX - Contractor Competitive Bidding & Bid-Tab Outlier Analysis Engine
Evaluates procurement bids, unbalances, and statistical deviations from engineer estimates.
"""

from typing import Dict, List, Any
import math


class ContractorBiddingEngine:
    """
    Public works competitive bid evaluation and front-loading / unbalanced bid detection.
    """

    @classmethod
    def evaluate_bid_tabulation(
        cls,
        engineers_estimate: float,
        bids: List[Dict[str, Any]],  # [{"contractor_id": 1, "bid_amount": 100000.0, "is_responsive": True, "is_responsible": True}]
    ) -> Dict[str, Any]:
        if not bids:
            return {"status": "NO_BIDS"}

        valid_bids = [b for b in bids if b.get("is_responsive", True) and b.get("is_responsible", True)]
        if not valid_bids:
            return {"status": "NO_RESPONSIVE_BIDS"}

        # Sort by bid amount
        sorted_bids = sorted(valid_bids, key=lambda x: x["bid_amount"])
        lowest_bid = sorted_bids[0]
        
        amounts = [b["bid_amount"] for b in valid_bids]
        mean_bid = sum(amounts) / len(amounts)
        variance = sum((x - mean_bid) ** 2 for x in amounts) / len(amounts) if len(amounts) > 1 else 0.0
        std_dev = math.sqrt(variance)

        variance_from_estimate_pct = ((lowest_bid["bid_amount"] - engineers_estimate) / engineers_estimate) * 100.0

        # Anomaly / Unusually low bid warning (more than 2 standard deviations below mean)
        potential_predatory_bid = lowest_bid["bid_amount"] < (mean_bid - 1.5 * std_dev) if len(amounts) >= 3 else False

        return {
            "selected_awardee_contractor_id": lowest_bid.get("contractor_id"),
            "winning_bid_amount": lowest_bid["bid_amount"],
            "engineers_estimate": engineers_estimate,
            "variance_from_engineers_estimate_pct": round(variance_from_estimate_pct, 2),
            "bid_spread_mean": round(mean_bid, 2),
            "bid_spread_std_dev": round(std_dev, 2),
            "potential_unbalanced_predatory_bid": potential_predatory_bid,
            "total_bids_received": len(bids),
            "valid_responsive_bids_count": len(valid_bids),
        }
