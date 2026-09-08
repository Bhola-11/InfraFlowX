"""
Building Engineering & Sustainability Engine
Implements Facility Condition Index (FCI), ASTM E2018 Property Condition Assessments,
and ASHRAE Level 1 Energy Utilization Index (EUI) estimations.
"""
from decimal import Decimal


class FacilityConditionIndexEngine:
    """
    Computes FCI = (Total Deferred Maintenance & Repair Needs) / (Current Building Replacement Value)
    FCI Rating Benchmarks:
    0.00 - 0.05: Good / Excellent condition
    0.06 - 0.10: Fair condition
    0.11 - 0.30: Poor condition
    > 0.30: Critical / Comprehensive Renovation Required
    """
    @staticmethod
    def calculate_fci(total_repair_needs_cost, current_replacement_value):
        crv = Decimal(str(current_replacement_value))
        repairs = Decimal(str(total_repair_needs_cost))
        if crv <= 0:
            return Decimal('0.000')
        fci = repairs / crv
        return round(fci, 3)

    @staticmethod
    def get_fci_status(fci_value):
        v = float(fci_value)
        if v <= 0.05:
            return {'status': 'GOOD', 'rating': 'Good / Sound Structural Condition', 'color': 'success'}
        elif v <= 0.10:
            return {'status': 'FAIR', 'rating': 'Fair / Moderate Deferred Maintenance', 'color': 'warning'}
        elif v <= 0.30:
            return {'status': 'POOR', 'rating': 'Poor / Significant Capital Renewal Needed', 'color': 'danger'}
        else:
            return {'status': 'CRITICAL', 'rating': 'Critical / Renovation or Replacement Mandated', 'color': 'dark'}


class BuildingEnergyEngine:
    """
    ASHRAE Energy Utilization Index (EUI in kBtu/sqft/yr) and Carbon Emissions Estimator.
    """
    @staticmethod
    def estimate_annual_eui(total_kwh_electricity, total_therms_gas, gross_area_sqft):
        area = float(gross_area_sqft)
        if area <= 0:
            return Decimal('0.00')
        # 1 kWh = 3.412 kBtu; 1 Therm = 99.976 kBtu
        total_kbtu = (float(total_kwh_electricity) * 3.412) + (float(total_therms_gas) * 99.976)
        eui = total_kbtu / area
        return round(Decimal(str(eui)), 2)

    @staticmethod
    def calculate_greenhouse_emissions_metric_tons(total_kwh_electricity, total_therms_gas):
        # US EPA emission factors: 0.000386 MT CO2e / kWh; 0.0053 MT CO2e / Therm
        mt_co2 = (float(total_kwh_electricity) * 0.000386) + (float(total_therms_gas) * 0.0053)
        return round(Decimal(str(mt_co2)), 2)
