"""
InfraFlowX - Traffic Flow and Highway Capacity Engineering Engine
Compliant with Highway Capacity Manual (HCM) 6th Edition & Lighthill-Whitham-Richards (LWR) Shockwave Theory.
"""

from typing import Dict, List, Any, Optional, Tuple
import math
from dataclasses import dataclass, field


@dataclass
class TrafficStreamParameters:
    free_flow_speed: float  # km/h
    jam_density: float  # vehicles/km/lane
    capacity: float  # vehicles/hour/lane
    number_of_lanes: int = 2
    lane_width_m: float = 3.65
    lateral_clearance_m: float = 1.8
    heavy_vehicle_percentage: float = 10.0
    terrain_type: str = "LEVEL"  # LEVEL, ROLLING, MOUNTAINOUS
    driver_population_factor: float = 1.0


class GreenshieldsModel:
    """
    Greenshields Linear Speed-Density Model:
    v(k) = v_f * (1 - k / k_j)
    q(k) = k * v(k) = v_f * k * (1 - k / k_j)
    q_max = v_f * k_j / 4
    """

    def __init__(self, free_flow_speed: float, jam_density: float):
        self.v_f = free_flow_speed
        self.k_j = jam_density
        self.k_crit = jam_density / 2.0
        self.q_max = (free_flow_speed * jam_density) / 4.0

    def speed_at_density(self, density_k: float) -> float:
        if density_k <= 0:
            return self.v_f
        if density_k >= self.k_j:
            return 0.0
        return self.v_f * (1.0 - (density_k / self.k_j))

    def flow_at_density(self, density_k: float) -> float:
        speed = self.speed_at_density(density_k)
        return density_k * speed

    def density_at_flow(self, flow_q: float) -> Tuple[float, float]:
        if flow_q > self.q_max:
            raise ValueError(f"Flow {flow_q:.1f} exceeds maximum capacity {self.q_max:.1f} veh/h/ln")
        discriminant = max(0.0, 1.0 - (4.0 * flow_q / (self.v_f * self.k_j)))
        k_uncongested = (self.k_j / 2.0) * (1.0 - math.sqrt(discriminant))
        k_congested = (self.k_j / 2.0) * (1.0 + math.sqrt(discriminant))
        return k_uncongested, k_congested


class GreenbergModel:
    """
    Greenberg Logarithmic Speed-Density Model (optimally calibrated for congested regimes):
    v(k) = v_0 * ln(k_j / k)
    """

    def __init__(self, optimum_speed_v0: float, jam_density: float):
        self.v_0 = optimum_speed_v0
        self.k_j = jam_density

    def speed_at_density(self, density_k: float) -> float:
        if density_k <= 0.001:
            return self.v_0 * math.log(self.k_j / 0.001)
        if density_k >= self.k_j:
            return 0.0
        return self.v_0 * math.log(self.k_j / density_k)

    def flow_at_density(self, density_k: float) -> float:
        return density_k * self.speed_at_density(density_k)


class LWRShockwaveEngine:
    """
    Lighthill-Whitham-Richards Shockwave Speed Calculator.
    Shockwave velocity: w = (q_b - q_a) / (k_b - k_a)
    Determines queue propagation, bottleneck clearing times, and dissipation fronts.
    """

    def __init__(self, greenshields: GreenshieldsModel):
        self.model = greenshields

    def compute_shockwave_speed(self, k_upstream: float, k_downstream: float) -> float:
        if abs(k_downstream - k_upstream) < 1e-6:
            return self.model.v_f * (1.0 - 2.0 * k_upstream / self.model.k_j)
        q_up = self.model.flow_at_density(k_upstream)
        q_down = self.model.flow_at_density(k_downstream)
        return (q_down - q_up) / (k_downstream - k_upstream)

    def queue_growth_rate(self, arrival_flow: float, discharge_capacity: float) -> float:
        """Rate of queue length change in km/h."""
        k_up, _ = self.model.density_at_flow(min(arrival_flow, self.model.q_max))
        _, k_bottle = self.model.density_at_flow(min(discharge_capacity, self.model.q_max))
        return self.compute_shockwave_speed(k_up, k_bottle)

    def time_to_clear_queue(self, initial_queue_length_km: float, arrival_flow: float, capacity_cleared: float) -> float:
        """Returns dissipation time in hours."""
        k_arrive, _ = self.model.density_at_flow(min(arrival_flow, self.model.q_max))
        _, k_jammed = self.model.density_at_flow(min(arrival_flow * 0.9, self.model.q_max))
        recovery_speed = self.compute_shockwave_speed(self.model.k_crit, k_arrive)
        if recovery_speed >= 0:
            return initial_queue_length_km / max(0.1, abs(recovery_speed))
        return initial_queue_length_km / abs(recovery_speed)


class HCMHighwayCapacityAnalyzer:
    """
    Highway Capacity Manual (HCM) Multilane Highway and Freeway Segment Evaluator.
    Computes Free Flow Speed adjustments, 15-minute Peak Flow Rate, and Level of Service (LOS).
    """

    def __init__(self, params: TrafficStreamParameters):
        self.p = params

    def calculate_adjusted_free_flow_speed(self) -> float:
        # FFS = BFFS - f_LW - f_TLC - f_M - f_A
        # Base Free Flow Speed
        bffs = self.p.free_flow_speed
        
        # Lane width adjustment
        if self.p.lane_width_m >= 3.6:
            f_lw = 0.0
        elif self.p.lane_width_m >= 3.3:
            f_lw = 3.1
        elif self.p.lane_width_m >= 3.0:
            f_lw = 10.6
        else:
            f_lw = 15.0

        # Total lateral clearance adjustment
        tlc = self.p.lateral_clearance_m * 2.0
        if tlc >= 3.6:
            f_tlc = 0.0
        elif tlc >= 2.4:
            f_tlc = 1.9
        elif tlc >= 1.2:
            f_tlc = 4.5
        else:
            f_tlc = 8.7

        # Heavy vehicle passenger car equivalent (PCE)
        p_t = self.p.heavy_vehicle_percentage / 100.0
        e_t = 1.5 if self.p.terrain_type == "LEVEL" else (2.5 if self.p.terrain_type == "ROLLING" else 4.5)
        f_hv = 1.0 / (1.0 + p_t * (e_t - 1.0))

        adjusted_ffs = max(60.0, bffs - f_lw - f_tlc)
        return adjusted_ffs

    def calculate_peak_15min_flow_rate(self, hourly_volume: float, peak_hour_factor: float = 0.92) -> float:
        # v_p = V / (PHF * N * f_HV * f_p)
        p_t = self.p.heavy_vehicle_percentage / 100.0
        e_t = 1.5 if self.p.terrain_type == "LEVEL" else (2.5 if self.p.terrain_type == "ROLLING" else 4.5)
        f_hv = 1.0 / (1.0 + p_t * (e_t - 1.0))
        
        v_p = hourly_volume / (peak_hour_factor * self.p.number_of_lanes * f_hv * self.p.driver_population_factor)
        return v_p

    def evaluate_level_of_service(self, hourly_volume: float, peak_hour_factor: float = 0.92) -> Dict[str, Any]:
        ffs = self.calculate_adjusted_free_flow_speed()
        v_p = self.calculate_peak_15min_flow_rate(hourly_volume, peak_hour_factor)
        
        # Density D = v_p / S
        # Speed flow curve breakpoints from HCM
        if v_p <= 1400:
            speed = ffs
        else:
            speed = ffs - ((ffs - (ffs * 0.75)) * ((v_p - 1400) / (2400 - 1400)) ** 2)
            speed = max(40.0, speed)
            
        density = v_p / speed  # passenger cars per km per lane
        
        # LOS Thresholds based on density
        if density <= 7:
            los = "A"
            status = "Free Flow"
        elif density <= 11:
            los = "B"
            status = "Reasonably Free Flow"
        elif density <= 16:
            los = "C"
            status = "Stable Operation"
        elif density <= 22:
            los = "D"
            status = "Approaching Unstable"
        elif density <= 28:
            los = "E"
            status = "Unstable Capacity Operation"
        else:
            los = "F"
            status = "Breakdown / Congested Queue"

        vc_ratio = v_p / 2400.0

        return {
            "level_of_service": los,
            "status_description": status,
            "density_pc_km_ln": round(density, 2),
            "operating_speed_kmh": round(speed, 2),
            "peak_flow_rate_pcphpl": round(v_p, 2),
            "adjusted_free_flow_speed": round(ffs, 2),
            "volume_capacity_ratio": round(vc_ratio, 3),
            "capacity_remaining_pcphpl": round(max(0.0, 2400.0 - v_p), 2),
        }
