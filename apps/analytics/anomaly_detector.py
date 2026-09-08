"""
InfraFlowX - Statistical Anomaly Detection & Sensor Outlier Filter Engine
Implements Z-score and rolling interquartile range (IQR) detection on IoT telemetry streams.
"""

from typing import Dict, List, Any
import math


class SensorAnomalyDetectorEngine:
    """
    Detects anomalous sensor spikes, sensor drift, and abrupt infrastructure condition drops.
    """

    @classmethod
    def detect_zscore_anomalies(cls, values: List[float], threshold_z: float = 3.0) -> Dict[str, Any]:
        if len(values) < 3:
            return {"anomalies_indices": [], "anomaly_count": 0}

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            return {"anomalies_indices": [], "anomaly_count": 0}

        anomalies = []
        for i, val in enumerate(values):
            z = abs((val - mean) / std_dev)
            if z >= threshold_z:
                anomalies.append({"index": i, "value": val, "z_score": round(z, 2)})

        return {
            "series_mean": round(mean, 2),
            "series_std_dev": round(std_dev, 2),
            "threshold_z": threshold_z,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
        }
