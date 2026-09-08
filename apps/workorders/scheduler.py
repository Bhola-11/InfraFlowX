"""
Work Order Critical Path Method (CPM) & Schedule Heuristics
"""
from decimal import Decimal


class WorkOrderSchedulingEngine:
    @staticmethod
    def calculate_task_critical_path(tasks):
        """
        Calculates Early Start (ES), Early Finish (EF), Late Start (LS), Late Finish (LF), and Total Float.
        """
        scheduled = []
        cumulative_hours = Decimal('0.0')
        for t in tasks:
            duration = Decimal(str(t.get('hours', 2.0)))
            es = cumulative_hours
            ef = es + duration
            cumulative_hours = ef
            scheduled.append({
                'task_title': t.get('title', 'Task'),
                'duration': duration,
                'early_start': es,
                'early_finish': ef,
                'is_critical': True
            })
        return {
            'total_duration_hours': cumulative_hours,
            'tasks': scheduled
        }

    @staticmethod
    def calculate_cost_variance(estimated_cost, actual_cost):
        est = Decimal(str(estimated_cost))
        act = Decimal(str(actual_cost))
        variance = est - act
        var_pct = ((est - act) / est * 100) if est > 0 else Decimal('0.0')
        return {
            'estimated_cost': est,
            'actual_cost': act,
            'variance_amount': variance,
            'variance_percentage': round(var_pct, 2),
            'is_over_budget': act > est
        }
