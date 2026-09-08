"""
Reliability Centered Maintenance (RCM) & Failure Mode and Effects Analysis (FMEA)
Calculates Risk Priority Numbers (RPN = Severity x Occurrence x Detection) and optimum maintenance intervals.
"""
from decimal import Decimal
import math


class RCMEngine:
    @staticmethod
    def calculate_rpn(severity_1_to_10, occurrence_1_to_10, detection_1_to_10):
        s = max(1, min(10, int(severity_1_to_10)))
        o = max(1, min(10, int(occurrence_1_to_10)))
        d = max(1, min(10, int(detection_1_to_10)))
        rpn = s * o * d
        
        if rpn >= 200:
            crit = {'level': 'CRITICAL', 'color': 'danger', 'action': 'Immediate Redesign or Daily Condition Monitoring'}
        elif rpn >= 100:
            crit = {'level': 'HIGH', 'color': 'warning', 'action': 'Weekly Preventive Overhaul Schedule'}
        elif rpn >= 40:
            crit = {'level': 'MEDIUM', 'color': 'info', 'action': 'Standard Cyclic Maintenance'}
        else:
            crit = {'level': 'LOW', 'color': 'success', 'action': 'Run-to-Failure Acceptable'}
            
        return {
            'severity': s,
            'occurrence': o,
            'detection': d,
            'rpn': rpn,
            'criticality': crit
        }

    @staticmethod
    def calculate_optimum_preventive_interval(mtbf_hours, repair_cost_usd, failure_cost_usd):
        """
        Cost-optimum replacement interval using age replacement model:
        T_opt = MTBF * (C_p / C_f)^0.5
        """
        mtbf = float(mtbf_hours)
        c_p = max(1.0, float(repair_cost_usd))
        c_f = max(c_p, float(failure_cost_usd))
        
        ratio = c_p / c_f
        t_opt = mtbf * math.sqrt(ratio)
        return round(Decimal(str(t_opt)), 1)
