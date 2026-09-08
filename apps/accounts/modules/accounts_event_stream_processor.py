"""
InfraFlowX Enterprise Platform - Accounts Event Stream Processor & Sliding Window
Aggregates high-frequency telemetry events in temporal sliding windows.
"""

from typing import Dict, List, Any


class AccountsEventStreamProcessor:
    """
    Sliding window event stream aggregator for accounts.
    """

    @classmethod
    def aggregate_sliding_window(cls, event_stream: List[Dict[str, float]], window_size: int = 10) -> Dict[str, Any]:
        if not event_stream:
            return {"window_count": 0, "moving_averages": []}

        values = [e.get("value", 0.0) for e in event_stream]
        moving_avgs = []

        for i in range(len(values)):
            start_idx = max(0, i - window_size + 1)
            window_slice = values[start_idx:i + 1]
            avg = sum(window_slice) / len(window_slice)
            moving_avgs.append(round(avg, 3))

        return {
            "app_module": "accounts",
            "total_events_processed": len(event_stream),
            "window_size": window_size,
            "moving_averages": moving_avgs,
            "current_smoothed_value": moving_avgs[-1] if moving_avgs else 0.0,
        }
