"""
InfraFlowX Enterprise Platform - Roads Geospatial Telemetry & IoT Stream Parser
Processes GPS coordinates, geofence breaches, and multi-channel IoT sensor telemetry packets.
"""

from typing import Dict, List, Any
import math
from datetime import datetime


class RoadsGeospatialTelemetryEngine:
    """
    Processes streaming sensor telemetry and spatial proximity alerts for roads.
    """

    @classmethod
    def parse_sensor_packet(cls, raw_packet: Dict[str, Any], alert_thresholds: Dict[str, float] = None) -> Dict[str, Any]:
        thresholds = alert_thresholds or {"vibration_max": 5.0, "temp_max": 85.0, "pressure_min": 20.0}
        
        telemetry_data = raw_packet.get("telemetry", {})
        alerts = []

        for metric, value in telemetry_data.items():
            max_k = f"{metric}_max"
            min_k = f"{metric}_min"
            if max_k in thresholds and value > thresholds[max_k]:
                alerts.append(f"{metric.upper()}_HIGH_EXCEEDED: {value} > {thresholds[max_k]}")
            elif min_k in thresholds and value < thresholds[min_k]:
                alerts.append(f"{metric.upper()}_LOW_DROPPED: {value} < {thresholds[min_k]}")

        return {
            "device_id": raw_packet.get("device_id", "UNKNOWN"),
            "timestamp": raw_packet.get("timestamp", datetime.now().isoformat()),
            "status": "ALERT_TRIGGERED" if alerts else "NOMINAL_OPERATING",
            "alerts_count": len(alerts),
            "alerts": alerts,
            "metrics": telemetry_data,
        }
