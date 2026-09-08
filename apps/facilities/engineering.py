"""
Facility Equipment Reliability & MTBF / MTTR Engineering Engine
Implements IEEE 493 Gold Book reliability standards, Weibull cumulative failure probability,
and Overall Equipment Effectiveness (OEE) metrics.
"""
from decimal import Decimal
import math


class EquipmentReliabilityEngine:
    @staticmethod
    def calculate_mtbf_mttr(total_operating_hours, failure_count, total_downtime_hours):
        """
        MTBF = (Operating Hours - Downtime Hours) / Number of Failures
        MTTR = Total Downtime Hours / Number of Failures
        Availability = MTBF / (MTBF + MTTR)
        """
        ops = float(total_operating_hours)
        fails = max(1, int(failure_count))
        down = float(total_downtime_hours)
        
        uptime = max(0.0, ops - down)
        mtbf = uptime / fails
        mttr = down / fails
        
        availability = (mtbf / (mtbf + mttr)) * 100.0 if (mtbf + mttr) > 0 else 100.0
        
        return {
            'mtbf_hours': round(Decimal(str(mtbf)), 1),
            'mttr_hours': round(Decimal(str(mttr)), 1),
            'availability_pct': round(Decimal(str(min(100.0, availability))), 2)
        }

    @staticmethod
    def calculate_weibull_failure_probability(operating_hours, characteristic_life_eta, shape_parameter_beta=1.5):
        """
        Cumulative Weibull Failure Distribution:
        F(t) = 1 - exp(-(t / eta)^beta)
        """
        t = float(operating_hours)
        eta = max(1.0, float(characteristic_life_eta))
        beta = float(shape_parameter_beta)
        
        f_t = 1.0 - math.exp(-((t / eta)**beta))
        return round(Decimal(str(min(1.0, max(0.0, f_t)))), 4)

    @staticmethod
    def calculate_oee(availability_pct, performance_pct, quality_pct):
        """
        OEE = Availability * Performance * Quality
        """
        a = float(availability_pct) / 100.0
        p = float(performance_pct) / 100.0
        q = float(quality_pct) / 100.0
        oee = (a * p * q) * 100.0
        return round(Decimal(str(oee)), 2)
