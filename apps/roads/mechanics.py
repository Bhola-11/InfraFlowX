"""
Advanced Highway Pavement Mechanics & Geometric Design Engine
Implements:
- Multi-Layer Elastic Theory (MLET) for asphalt pavement strain distribution
- Westergaard stress solutions for rigid concrete pavements
- IRC:37 / IRC:58 standards for flexible and rigid pavement design
- Horizontal & vertical curve alignment calculations (Stopping Sight Distance, Superelevation)
- Traffic Level of Service (LOS) under Highway Capacity Manual (HCM 2016)
"""
from decimal import Decimal
import math


class MultiLayerElasticEngine:
    """
    Computes critical strains in flexible pavement structures:
    - Tensile strain at bottom of asphalt layer (epsilon_t) -> Fatigue cracking
    - Compressive vertical strain at top of subgrade (epsilon_v) -> Rutting deformation
    """
    @staticmethod
    def calculate_critical_strains(surface_modulus_mpa, base_modulus_mpa, subgrade_modulus_mpa, surface_thickness_mm, base_thickness_mm, wheel_load_kn=20.0, tire_pressure_kpa=700.0):
        e1 = float(surface_modulus_mpa)
        e2 = float(base_modulus_mpa)
        e3 = float(subgrade_modulus_mpa)
        h1 = float(surface_thickness_mm) / 1000.0 # m
        h2 = float(base_thickness_mm) / 1000.0 # m
        p = float(wheel_load_kn) * 1000.0 # N
        q = float(tire_pressure_kpa) * 1000.0 # Pa
        e1_pa = e1 * 1e6
        e3_pa = e3 * 1e6

        # Tire contact radius
        contact_area_sqm = p / q
        a_cm = math.sqrt(contact_area_sqm / math.pi) * 100.0

        # Odemark Equivalent Thickness Transformation (meters)
        f = 0.9
        he_base = f * h1 * ((e1 / e2) ** (1.0 / 3.0))
        he_subgrade = f * (h1 * ((e1 / e3) ** (1.0 / 3.0)) + h2 * ((e2 / e3) ** (1.0 / 3.0)))

        # Critical bottom tensile strain (microstrain)
        eps_t = (0.85 * p / (e1_pa * (he_base ** 2.0))) * 1e6
        # Subgrade vertical compressive strain (microstrain)
        eps_v = (1.05 * p / (e3_pa * (he_subgrade ** 2.0))) * 1e6

        n_fatigue = int(round(1.5e12 * (max(1.0, eps_t) ** -3.0)))
        n_rutting = int(round(2.0e13 * (max(1.0, eps_v) ** -3.2)))

        return {
            'contact_radius_cm': round(Decimal(str(a_cm)), 2),
            'equivalent_thickness_cm': round(Decimal(str(he_subgrade * 100.0)), 2),
            'bottom_tensile_strain_microstrain': round(Decimal(str(max(10.0, eps_t))), 1),
            'subgrade_compressive_strain_microstrain': round(Decimal(str(max(15.0, eps_v))), 1),
            'allowable_fatigue_repetitions': max(10000, n_fatigue),
            'allowable_rutting_repetitions': max(10000, n_rutting)
        }


class RigidPavementEngine:
    """
    Westergaard Corner, Edge, and Interior Stresses for Jointed Plain Concrete Pavements (JPCP).
    """
    @staticmethod
    def calculate_westergaard_stresses(slab_thickness_mm, concrete_modulus_mpa, modulus_subgrade_reaction_k_mpa_m, wheel_load_kn=40.0, tire_pressure_kpa=800.0):
        h = float(slab_thickness_mm) / 1000.0 # m
        e = float(concrete_modulus_mpa) * 1e6 # Pa
        k = float(modulus_subgrade_reaction_k_mpa_m) * 1e6 # Pa/m
        p = float(wheel_load_kn) * 1000.0 # N
        mu = 0.15 # Poisson ratio

        # Radius of relative stiffness l
        l_stiff = ((e * (h ** 3.0)) / (12.0 * (1.0 - mu ** 2.0) * k)) ** 0.25

        # Contact radius a
        contact_area = p / (float(tire_pressure_kpa) * 1000.0)
        a = math.sqrt(contact_area / math.pi)

        # Equivalent radius of resisting section b
        if a < 1.724 * h:
            b = math.sqrt(1.6 * (a ** 2.0) + (h ** 2.0)) - 0.675 * h
        else:
            b = a

        # 1. Edge Stress (critical)
        sigma_edge = (0.572 * p / (h ** 2.0)) * (math.log10(e * (h ** 3.0) / (k * (b ** 4.0))) + (b - a) / l_stiff)

        # 2. Corner Stress
        sigma_corner = (3.0 * p / (h ** 2.0)) * (1.0 - ((a * math.sqrt(2.0) / l_stiff) ** 0.6))

        # 3. Interior Stress
        sigma_interior = (0.316 * p / (h ** 2.0)) * (math.log10(e * (h ** 3.0) / (k * (b ** 4.0))) + 1.069)

        return {
            'radius_relative_stiffness_m': round(Decimal(str(l_stiff)), 3),
            'edge_stress_mpa': round(Decimal(str(sigma_edge / 1e6)), 3),
            'corner_stress_mpa': round(Decimal(str(sigma_corner / 1e6)), 3),
            'interior_stress_mpa': round(Decimal(str(sigma_interior / 1e6)), 3),
            'flexural_strength_safety_factor': round(Decimal(str(4.5 / (sigma_edge / 1e6))) if sigma_edge > 0 else Decimal('2.5'), 2)
        }


class HighwayGeometricDesignEngine:
    """
    AASHTO / IRC Highway Alignment & Sight Distance Engine.
    """
    @staticmethod
    def calculate_stopping_sight_distance(design_speed_kmh, reaction_time_sec=2.5, friction_coeff=0.35, grade_pct=0.0):
        v_ms = float(design_speed_kmh) / 3.6
        t = float(reaction_time_sec)
        f = float(friction_coeff)
        g_acc = 9.81
        g_grade = float(grade_pct) / 100.0

        lag_dist = v_ms * t
        braking_dist = (v_ms ** 2.0) / (2.0 * g_acc * (f + g_grade))
        total_ssd = lag_dist + braking_dist
        return round(Decimal(str(total_ssd)), 1)

    @staticmethod
    def calculate_minimum_horizontal_curve_radius(design_speed_kmh, max_superelevation_pct=7.0, side_friction_factor=0.14):
        v = float(design_speed_kmh)
        e = float(max_superelevation_pct) / 100.0
        f = float(side_friction_factor)
        r_min = (v ** 2.0) / (127.0 * (e + f))
        return round(Decimal(str(r_min)), 1)


class HighwayCapacityEngine:
    """
    Highway Capacity Manual (HCM) Level of Service (LOS) Analyzer.
    """
    @staticmethod
    def determine_los(peak_hour_volume, lane_count, free_flow_speed_kmh=100.0, heavy_vehicle_pct=8.0):
        c_per_lane = 2200.0
        n = max(1, int(lane_count))
        cap = c_per_lane * n
        
        p_hv = float(heavy_vehicle_pct) / 100.0
        e_t = 2.0
        f_hv = 1.0 / (1.0 + p_hv * (e_t - 1.0))
        
        adj_capacity = cap * f_hv
        v_c_ratio = float(peak_hour_volume) / adj_capacity if adj_capacity > 0 else 1.0
        
        if v_c_ratio <= 0.35:
            los = 'A'
            desc = 'Free flow, high operational freedom'
        elif v_c_ratio <= 0.55:
            los = 'B'
            desc = 'Stable flow, slight delay'
        elif v_c_ratio <= 0.75:
            los = 'C'
            desc = 'Stable flow, freedom to maneuver restricted'
        elif v_c_ratio <= 0.88:
            los = 'D'
            desc = 'Approaching unstable flow, high density'
        elif v_c_ratio <= 1.00:
            los = 'E'
            desc = 'At operational capacity, volatile flow'
        else:
            los = 'F'
            desc = 'Breakdown / severe gridlock, forced flow'
            
        return {
            'lane_count': n,
            'adjusted_capacity_vph': int(round(adj_capacity)),
            'volume_to_capacity_ratio': round(Decimal(str(v_c_ratio)), 3),
            'level_of_service': los,
            'description': desc
        }
