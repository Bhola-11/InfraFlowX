"""
InfraFlowX - Structural Health Monitoring (SHM) & Bridge Sensor Analytics Engine
Implements Rainflow Cycle Counting and Dynamic Vibration Spectral Analysis.
"""

from typing import Dict, List, Any, Tuple
import math


class RainflowCycleCounter:
    """
    ASTM E1049-85 Standard Practice for Cycle Counting in Fatigue Analysis.
    Extracts stress cycle ranges and means from complex time-series strain sensor data.
    """

    @classmethod
    def extract_reversal_points(cls, signal: List[float]) -> List[float]:
        if len(signal) < 3:
            return signal
        peaks = [signal[0]]
        for i in range(1, len(signal) - 1):
            if (signal[i] > signal[i - 1] and signal[i] > signal[i + 1]) or (signal[i] < signal[i - 1] and signal[i] < signal[i + 1]):
                peaks.append(signal[i])
        peaks.append(signal[-1])
        return peaks

    @classmethod
    def count_cycles(cls, stress_series: List[float]) -> List[Dict[str, float]]:
        extrema = cls.extract_reversal_points(stress_series)
        cycles = []
        stack = []

        for p in extrema:
            stack.append(p)
            while len(stack) >= 3:
                s0 = stack[-3]
                s1 = stack[-2]
                s2 = stack[-1]
                
                delta_y = abs(s1 - s0)
                delta_x = abs(s2 - s1)
                
                if delta_x >= delta_y:
                    mean_val = (s0 + s1) / 2.0
                    cycles.append({
                        "range_mpa": round(delta_y, 3),
                        "mean_mpa": round(mean_val, 3),
                        "cycle_count": 1.0,
                    })
                    stack.pop(-2)
                    stack.pop(-2)
                else:
                    break

        return cycles


class DynamicVibrationAnalyzer:
    """
    Vibration spectral modal extraction and Dynamic Amplification Factor (DAF).
    """

    @classmethod
    def dynamic_amplification_factor(cls, max_dynamic_strain: float, static_strain: float) -> float:
        """DAF = Max Dynamic Response / Static Response"""
        if static_strain <= 0:
            return 1.0
        return round(max_dynamic_strain / static_strain, 3)

    @classmethod
    def estimate_fundamental_frequency(cls, span_length_m: float, structural_type: str = "STEEL_GIRDER") -> float:
        """
        Empirical structural frequency estimation: f_0 ~ C / L^1.3
        """
        coeff = 85.0 if "CONCRETE" in structural_type.upper() else 110.0
        f_0 = coeff / (max(5.0, span_length_m) ** 1.15)
        return round(f_0, 2)
