"""
InfraFlowX Enterprise Platform - Inventory Digital Twin & Cyber-Physical Synchronizer
Maintains live cyber-physical state models, state-space representations, and sensor telemetry sync.
"""

from typing import Dict, List, Any
import math
from datetime import datetime


class InventoryDigitalTwinEngine:
    """
    Digital twin simulation and state-space telemetry synchronization for inventory.
    """

    @classmethod
    def update_twin_state(cls, previous_state: Dict[str, float], sensor_inputs: Dict[str, float], damping_factor: float = 0.85) -> Dict[str, Any]:
        """
        Updates virtual twin state using exponential moving average state estimation.
        x_new = damping * x_old + (1 - damping) * z_sensor
        """
        updated_state = {}
        state_deltas = {}

        all_keys = set(previous_state.keys()).union(set(sensor_inputs.keys()))
        for k in all_keys:
            old_v = previous_state.get(k, 0.0)
            new_v = sensor_inputs.get(k, old_v)
            filtered_v = damping_factor * old_v + (1.0 - damping_factor) * new_v
            
            updated_state[k] = round(filtered_v, 3)
            state_deltas[k] = round(filtered_v - old_v, 3)

        return {
            "app_module": "inventory",
            "synchronized_at": datetime.now().isoformat(),
            "virtual_state": updated_state,
            "state_deltas": state_deltas,
            "convergence_stable": all(abs(d) < 50.0 for d in state_deltas.values()),
        }
