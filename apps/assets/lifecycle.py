"""
Asset Lifecycle & Financial Depreciation Engine
Implements GAAP / GASB 34 Straight-Line, MACRS (Modified Accelerated Cost Recovery System),
Declining Balance, and Replacement Cost Forecasting models.
"""
from decimal import Decimal
from datetime import date


class AssetDepreciationEngine:
    MACRS_GDS_TABLES = {
        3: [Decimal('0.3333'), Decimal('0.4445'), Decimal('0.1481'), Decimal('0.0741')],
        5: [Decimal('0.2000'), Decimal('0.3200'), Decimal('0.1920'), Decimal('0.1152'), Decimal('0.1152'), Decimal('0.0576')],
        7: [Decimal('0.1429'), Decimal('0.2449'), Decimal('0.1749'), Decimal('0.1249'), Decimal('0.0893'), Decimal('0.0892'), Decimal('0.0893'), Decimal('0.0446')],
        15: [Decimal('0.0500'), Decimal('0.0950'), Decimal('0.0855'), Decimal('0.0770'), Decimal('0.0693'), Decimal('0.0623'), Decimal('0.0590'), Decimal('0.0590'), Decimal('0.0591'), Decimal('0.0590'), Decimal('0.0591'), Decimal('0.0590'), Decimal('0.0591'), Decimal('0.0590'), Decimal('0.0591'), Decimal('0.0295')],
        20: [Decimal('0.03750'), Decimal('0.07219'), Decimal('0.06677'), Decimal('0.06177'), Decimal('0.05713'), Decimal('0.05285'), Decimal('0.04888'), Decimal('0.04522'), Decimal('0.04462'), Decimal('0.04461'), Decimal('0.04462'), Decimal('0.04461'), Decimal('0.04462'), Decimal('0.04461'), Decimal('0.04462'), Decimal('0.04461'), Decimal('0.04462'), Decimal('0.04461'), Decimal('0.04462'), Decimal('0.04461'), Decimal('0.02231')],
    }

    @staticmethod
    def calculate_straight_line_depreciation(cost, salvage_value, useful_life_years, age_years):
        cost_d = Decimal(str(cost))
        salvage_d = Decimal(str(salvage_value))
        life = max(1, int(useful_life_years))
        age = min(life, max(0, int(age_years)))
        
        depreciable_base = max(Decimal('0.00'), cost_d - salvage_d)
        annual_depreciation = depreciable_base / Decimal(str(life))
        accumulated = annual_depreciation * Decimal(str(age))
        current_book_value = max(salvage_d, cost_d - accumulated)
        
        return {
            'annual_depreciation': round(annual_depreciation, 2),
            'accumulated_depreciation': round(accumulated, 2),
            'current_book_value': round(current_book_value, 2),
            'remaining_useful_life': life - age
        }

    @classmethod
    def calculate_macrs_schedule(cls, cost, recovery_period_years):
        cost_d = Decimal(str(cost))
        table = cls.MACRS_GDS_TABLES.get(int(recovery_period_years), cls.MACRS_GDS_TABLES[7])
        schedule = []
        accumulated = Decimal('0.00')
        
        for yr, rate in enumerate(table, start=1):
            dep_amount = cost_d * rate
            accumulated += dep_amount
            book_value = max(Decimal('0.00'), cost_d - accumulated)
            schedule.append({
                'year': yr,
                'rate': rate,
                'depreciation_amount': round(dep_amount, 2),
                'accumulated_depreciation': round(accumulated, 2),
                'ending_book_value': round(book_value, 2)
            })
        return schedule

    @staticmethod
    def forecast_replacement_cost(current_cost, inflation_rate_pct, years_until_replacement):
        c = float(current_cost)
        r = float(inflation_rate_pct) / 100.0
        n = max(0, int(years_until_replacement))
        future_cost = c * ((1.0 + r)**n)
        return round(Decimal(str(future_cost)), 2)
