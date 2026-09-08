"""
Critical Chain Project Management (CCPM) & Project Buffer Health
Implements Goldratt's Theory of Constraints (TOC) buffer consumption tracking (Fever Chart).
"""
from decimal import Decimal


class CriticalChainBufferEngine:
    @staticmethod
    def evaluate_buffer_health(project_progress_pct, buffer_consumed_pct):
        p_pct = float(project_progress_pct)
        b_pct = float(buffer_consumed_pct)

        # Fever chart zones (Green, Yellow, Red)
        # Red line: Buffer% > Progress% + 20%
        # Yellow line: Buffer% > Progress% - 10%
        if b_pct > p_pct + 20.0:
            zone = 'RED'
            status = 'CRITICAL_DELAY_RISK'
            action = 'Emergency task acceleration and resource mobilization required.'
        elif b_pct > p_pct - 10.0:
            zone = 'YELLOW'
            status = 'WARNING_MONITORING'
            action = 'Evaluate upcoming task dependencies and eliminate bottlenecks.'
        else:
            zone = 'GREEN'
            status = 'HEALTHY_ON_TRACK'
            action = 'Schedule execution proceeding according to target buffer.'

        return {
            'project_progress_pct': round(Decimal(str(p_pct)), 1),
            'buffer_consumed_pct': round(Decimal(str(b_pct)), 1),
            'fever_chart_zone': zone,
            'status': status,
            'recommended_action': action
        }
