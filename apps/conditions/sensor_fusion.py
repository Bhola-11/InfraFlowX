"""
InfraFlowX - Multi-Sensor Condition Fusion & 1D Kalman Filter Engine
Integrates disparate sensor observations (vibration, laser profilometer, strain, acoustic) into unified state estimates.
"""

from typing import Dict, List, Any, Tuple


class KalmanSensorFusionEngine:
    """
    1D Discrete Kalman Filter for Asset Condition Tracking.
    Estimates true condition score while filtering out measurement noise and drift.
    """

    def __init__(self, initial_state: float = 100.0, initial_variance: float = 1.0, process_noise_q: float = 0.05, measurement_noise_r: float = 0.8):
        self.x = initial_state
        self.p = initial_variance
        self.q = process_noise_q
        self.r = measurement_noise_r

    def predict(self, degradation_drift: float = -0.01) -> float:
        """Time update step."""
        self.x = self.x + degradation_drift
        self.p = self.p + self.q
        return self.x

    def update(self, measurement: float) -> Tuple[float, float]:
        """Measurement update step."""
        # Kalman Gain
        k_gain = self.p / (self.p + self.r)
        self.x = self.x + k_gain * (measurement - self.x)
        self.p = (1.0 - k_gain) * self.p
        return self.x, k_gain

    def process_sensor_stream(self, raw_measurements: List[float], annual_drift_per_step: float = -0.05) -> List[Dict[str, float]]:
        trajectory = []
        for i, z in enumerate(raw_measurements):
            pred_x = self.predict(annual_drift_per_step)
            filtered_x, gain = self.update(z)
            trajectory.append({
                "step": i + 1,
                "raw_measurement": round(z, 2),
                "predicted_prior": round(pred_x, 2),
                "kalman_estimated_condition": round(filtered_x, 2),
                "kalman_gain": round(gain, 4),
                "estimation_uncertainty": round(self.p, 4),
            })
        return trajectory
