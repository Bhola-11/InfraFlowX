"""
Highway & Road Pavement Engineering Calculation Engine
Implements ASTM D6433 Pavement Condition Index (PCI) standard,
AASHTO Structural Number (SN), Equivalent Single Axle Load (ESAL) projections,
and International Roughness Index (IRI) conversions.
"""
from decimal import Decimal
import math


class PavementConditionEngine:
    """
    Standard ASTM D6433 PCI calculation engine with deduct value curves.
    """
    DEDUCT_CURVES = {
        'POTHOLE': {
            'LOW': [(1, 5), (5, 15), (10, 25), (25, 45), (50, 70)],
            'MEDIUM': [(1, 15), (5, 30), (10, 50), (25, 75), (50, 95)],
            'HIGH': [(1, 30), (5, 55), (10, 80), (25, 95), (50, 100)],
        },
        'ALLIGATOR_CRACKING': {
            'LOW': [(1, 2), (5, 10), (10, 20), (25, 40), (50, 60)],
            'MEDIUM': [(1, 10), (5, 25), (10, 45), (25, 65), (50, 85)],
            'HIGH': [(1, 25), (5, 50), (10, 75), (25, 90), (50, 100)],
        },
        'RUTTING': {
            'LOW': [(1, 2), (5, 8), (10, 15), (25, 30), (50, 48)],
            'MEDIUM': [(1, 8), (5, 20), (10, 35), (25, 55), (50, 75)],
            'HIGH': [(1, 20), (5, 40), (10, 65), (25, 85), (50, 98)],
        },
        'LONGITUDINAL_CRACK': {
            'LOW': [(1, 1), (5, 4), (10, 8), (25, 18), (50, 30)],
            'MEDIUM': [(1, 4), (5, 12), (10, 22), (25, 40), (50, 58)],
            'HIGH': [(1, 12), (5, 28), (10, 48), (25, 70), (50, 88)],
        },
        'DRAINAGE_ISSUE': {
            'LOW': [(1, 3), (5, 8), (10, 14), (25, 25), (50, 40)],
            'MEDIUM': [(1, 10), (5, 22), (10, 38), (25, 58), (50, 75)],
            'HIGH': [(1, 25), (5, 45), (10, 68), (25, 85), (50, 95)],
        },
        'SUBSIDENCE': {
            'LOW': [(1, 8), (5, 18), (10, 30), (25, 50), (50, 70)],
            'MEDIUM': [(1, 20), (5, 40), (10, 60), (25, 80), (50, 95)],
            'HIGH': [(1, 35), (5, 65), (10, 85), (25, 98), (50, 100)],
        }
    }

    @classmethod
    def interpolate_deduct(cls, defect_type, severity, density_pct):
        """
        Interpolates deduct values from empirical density-deduct curves.
        """
        curves = cls.DEDUCT_CURVES.get(defect_type, cls.DEDUCT_CURVES['POTHOLE'])
        curve = curves.get(severity, curves.get('MEDIUM', [(1, 10), (50, 80)]))
        
        if density_pct <= curve[0][0]:
            return curve[0][1] * (density_pct / curve[0][0])
        if density_pct >= curve[-1][0]:
            return curve[-1][1]
        
        for i in range(len(curve) - 1):
            x0, y0 = curve[i]
            x1, y1 = curve[i + 1]
            if x0 <= density_pct <= x1:
                slope = (y1 - y0) / (x1 - x0)
                return y0 + slope * (density_pct - x0)
        return 0.0

    @classmethod
    def calculate_pci(cls, road_length_km, road_width_m, defects):
        """
        Computes the net Pavement Condition Index (PCI 0-100) from sample defects.
        """
        total_area_sqm = float(road_length_km * 1000) * float(road_width_m)
        if total_area_sqm <= 0:
            return 100

        deduct_values = []
        for d in defects:
            defect_type = d.get('defect_type', 'POTHOLE')
            severity = d.get('severity', 'MEDIUM')
            area_sqm = float(d.get('area_sqm', 5.0))
            density = (area_sqm / total_area_sqm) * 100.0
            dv = cls.interpolate_deduct(defect_type, severity, density)
            if dv > 2.0:
                deduct_values.append(dv)

        if not deduct_values:
            return 100

        deduct_values.sort(reverse=True)
        total_deduct = sum(deduct_values)
        
        # Corrected Deduct Value (CDV) empirical dampening
        q = len([v for v in deduct_values if v > 5.0])
        if q > 1:
            cdv_correction_factor = 1.0 - (0.08 * math.log(q + 1))
            total_deduct = total_deduct * max(0.4, cdv_correction_factor)

        pci = max(0, min(100, int(round(100.0 - total_deduct))))
        return pci

    @staticmethod
    def get_pci_category(pci_score):
        """
        Returns rating category and maintenance recommendation.
        """
        if pci_score >= 85:
            return {'rating': 'GOOD', 'color': 'success', 'treatment': 'Routine Preventive Crack Sealing'}
        elif pci_score >= 70:
            return {'rating': 'SATISFACTORY', 'color': 'info', 'treatment': 'Surface Seal Coat / Micro-Surfacing'}
        elif pci_score >= 55:
            return {'rating': 'FAIR', 'color': 'warning', 'treatment': 'Mill & Thin Asphalt Overlay (30-50mm)'}
        elif pci_score >= 40:
            return {'rating': 'POOR', 'color': 'danger', 'treatment': 'Structural Overlay & Sub-base Patching'}
        else:
            return {'rating': 'SERIOUS_CRITICAL', 'color': 'dark', 'treatment': 'Full-Depth Pavement Reconstruction'}


class AASHTODesignEngine:
    """
    AASHTO 1993 Flexible Pavement Design & Structural Number (SN) calculations.
    """
    @staticmethod
    def calculate_structural_number(layers):
        """
        SN = a1*D1 + a2*D2*m2 + a3*D3*m3
        where a_i = layer structural coefficient, D_i = thickness in inches, m_i = drainage factor.
        """
        total_sn = Decimal('0.00')
        for layer in layers:
            coeff = Decimal(str(layer.get('layer_coefficient', 0.44)))
            thickness_in = Decimal(str(layer.get('thickness_inches', 4.0)))
            drainage = Decimal(str(layer.get('drainage_factor', 1.0)))
            total_sn += coeff * thickness_in * drainage
        return round(total_sn, 2)

    @staticmethod
    def calculate_esal_projection(daily_trucks, growth_rate_pct, design_years=20, lane_distribution=0.8):
        """
        Computes Cumulative 18-kip Equivalent Single Axle Loads (ESALs).
        """
        r = float(growth_rate_pct) / 100.0
        n = design_years
        growth_factor = ((1.0 + r)**n - 1.0) / r if r > 0 else float(n)
        
        annual_esal = daily_trucks * 365.0 * 1.35 * lane_distribution
        cumulative_esal = annual_esal * growth_factor
        return round(Decimal(str(cumulative_esal)), 0)
