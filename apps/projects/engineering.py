"""
Capital Project Earned Value Management (EVM) Engine
Implements ANSI/EIA-748 Earned Value standard metrics:
- Planned Value (PV)
- Earned Value (EV = BAC * % Complete)
- Actual Cost (AC)
- Cost Variance (CV = EV - AC)
- Schedule Variance (SV = EV - PV)
- Cost Performance Index (CPI = EV / AC)
- Schedule Performance Index (SPI = EV / PV)
- Estimate at Completion (EAC = BAC / CPI)
"""
from decimal import Decimal


class EVMEngine:
    @staticmethod
    def calculate_evm_metrics(budget_at_completion, actual_cost, progress_percentage, planned_percentage=50):
        bac = Decimal(str(budget_at_completion))
        ac = Decimal(str(actual_cost))
        pct_comp = Decimal(str(progress_percentage)) / Decimal('100.0')
        pct_plan = Decimal(str(planned_percentage)) / Decimal('100.0')
        
        pv = bac * pct_plan
        ev = bac * pct_comp
        
        cv = ev - ac
        sv = ev - pv
        
        cpi = (ev / ac) if ac > 0 else Decimal('1.00')
        spi = (ev / pv) if pv > 0 else Decimal('1.00')
        
        eac = (bac / cpi) if cpi > 0 else bac
        vac = bac - eac
        
        return {
            'budget_at_completion': bac,
            'planned_value': round(pv, 2),
            'earned_value': round(ev, 2),
            'actual_cost': round(ac, 2),
            'cost_variance': round(cv, 2),
            'schedule_variance': round(sv, 2),
            'cpi': round(cpi, 3),
            'spi': round(spi, 3),
            'estimate_at_completion': round(eac, 2),
            'variance_at_completion': round(vac, 2),
            'is_cost_healthy': cpi >= Decimal('0.95'),
            'is_schedule_healthy': spi >= Decimal('0.95'),
        }
