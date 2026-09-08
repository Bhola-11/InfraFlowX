"""
Bridge Structural Engineering Calculation Engine
Implements FHWA National Bridge Inventory (NBI) Sufficiency Rating (SR),
Scour Criticality Vulnerability Index, and Live Load Rating (LRFR) evaluations.
"""
from decimal import Decimal
import math


class BridgeSufficiencyEngine:
    """
    Computes FHWA Bridge Sufficiency Rating (0 - 100%).
    Formula: SR = S1 + S2 + S3 - S4
    Where:
    S1 = Structural Adequacy & Safety (55% max)
    S2 = Serviceability & Functional Obsolescence (30% max)
    S3 = Essentiality for Public Use (15% max)
    S4 = Special Reductions (13% max)
    """
    @classmethod
    def calculate_sufficiency_rating(cls, bridge, deck_rating=7, super_rating=7, sub_rating=7, culvert_rating=None, detour_length_km=5.0, adt=15000):
        # S1: Structural Adequacy
        min_structural = min(deck_rating, super_rating, sub_rating)
        if culvert_rating is not None:
            min_structural = min(min_structural, culvert_rating)
            
        if min_structural >= 9:
            s1 = 55.0
        elif min_structural == 8:
            s1 = 50.0
        elif min_structural == 7:
            s1 = 45.0
        elif min_structural == 6:
            s1 = 38.0
        elif min_structural == 5:
            s1 = 30.0
        elif min_structural == 4:
            s1 = 20.0
        elif min_structural == 3:
            s1 = 10.0
        else:
            s1 = 0.0

        # S2: Serviceability & Functional Obsolescence
        s2 = 30.0
        if bridge.width_meters < 8.0:
            s2 -= 8.0
        if bridge.vertical_clearance_meters and bridge.vertical_clearance_meters < 4.5:
            s2 -= 10.0
        s2 = max(0.0, s2)

        # S3: Essentiality for Public Use
        # Based on ADT and detour length
        detour_factor = min(15.0, float(detour_length_km) * 0.5)
        traffic_factor = min(1.0, float(adt) / 20000.0)
        s3 = min(15.0, detour_factor * traffic_factor + 5.0)

        # S4: Special Reductions
        s4 = 0.0
        if bridge.is_scour_critical:
            s4 += 8.0
        if min_structural <= 3:
            s4 += 5.0

        net_sr = max(0.0, min(100.0, s1 + s2 + s3 - s4))
        return round(Decimal(str(net_sr)), 1)

    @staticmethod
    def get_federal_eligibility(sufficiency_rating):
        """
        FHWA Rehabilitation / Replacement eligibility thresholds.
        """
        sr = float(sufficiency_rating)
        if sr < 50.0:
            return {'status': 'ELIGIBLE_REPLACEMENT', 'label': 'Eligible for Federal Bridge Replacement Fund'}
        elif sr <= 80.0:
            return {'status': 'ELIGIBLE_REHABILITATION', 'label': 'Eligible for Federal Rehabilitation Grant'}
        else:
            return {'status': 'SATISFACTORY', 'label': 'Standard Preventive Maintenance Cycle'}


class BridgeScourEngine:
    """
    HEC-18 Scour at Bridges Geotechnical & Hydraulic Evaluation.
    """
    @staticmethod
    def calculate_pier_scour_depth(pier_width_m, flow_depth_m, flow_velocity_mps, bed_material_factor=1.1, nose_shape_factor=1.0):
        """
        Richardson CSU Pier Scour Equation:
        ys / y1 = 2.0 * K1 * K2 * K3 * K4 * (a / y1)^0.65 * Fr1^0.43
        """
        g = 9.81
        v = float(flow_velocity_mps)
        y1 = float(flow_depth_m)
        a = float(pier_width_m)
        
        froude = v / math.sqrt(g * y1) if y1 > 0 else 0.5
        froude = max(0.1, min(1.8, froude))
        
        k1 = float(nose_shape_factor)
        k2 = 1.0  # Angle of attack
        k3 = float(bed_material_factor)
        k4 = 1.0  # Armoring factor
        
        ratio = (a / y1) if y1 > 0 else 0.5
        ys_ratio = 2.0 * k1 * k2 * k3 * k4 * (ratio**0.65) * (froude**0.43)
        scour_depth = ys_ratio * y1
        return round(Decimal(str(scour_depth)), 2)
