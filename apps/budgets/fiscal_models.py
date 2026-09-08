"""
Multi-Year Capital Improvement Program (CIP) & Fiscal Velocity Engine
Implements:
- Capital Expenditure (CapEx) vs Operational Expenditure (OpEx) split optimization
- Fiscal variance tracking (Under-spending vs Over-obligation risk)
- Municipal bond debt service amortization schedules
"""
from decimal import Decimal
import math


class MunicipalFinanceEngine:
    @staticmethod
    def calculate_bond_amortization(bond_principal_amount, annual_coupon_rate_pct, maturity_years=20):
        p = float(bond_principal_amount)
        r = float(annual_coupon_rate_pct) / 100.0
        n = int(maturity_years)

        # Equal Annual Installment / Debt Service: A = P * [r(1+r)^n] / [(1+r)^n - 1]
        if r > 0:
            annual_payment = p * (r * ((1.0 + r) ** n)) / (((1.0 + r) ** n) - 1.0)
        else:
            annual_payment = p / float(n)

        schedule = []
        remaining_balance = p
        total_interest = 0.0

        for yr in range(1, n + 1):
            interest_portion = remaining_balance * r
            principal_portion = annual_payment - interest_portion
            remaining_balance = max(0.0, remaining_balance - principal_portion)
            total_interest += interest_portion

            schedule.append({
                'year': yr,
                'annual_debt_service': round(Decimal(str(annual_payment)), 2),
                'principal_paid': round(Decimal(str(principal_portion)), 2),
                'interest_paid': round(Decimal(str(interest_portion)), 2),
                'ending_balance': round(Decimal(str(remaining_balance)), 2)
            })

        return {
            'bond_principal': Decimal(str(round(p, 2))),
            'annual_debt_service': Decimal(str(round(annual_payment, 2))),
            'total_interest_paid': Decimal(str(round(total_interest, 2))),
            'total_repayment': Decimal(str(round(p + total_interest, 2))),
            'schedule': schedule
        }

    @staticmethod
    def evaluate_capex_velocity(allocated_amount, actual_spent, elapsed_fiscal_months=6):
        alloc = float(allocated_amount)
        spent = float(actual_spent)
        m = max(1, min(12, int(elapsed_fiscal_months)))

        expected_burn_pct = (m / 12.0) * 100.0
        actual_burn_pct = (spent / alloc * 100.0) if alloc > 0 else 0.0
        velocity_ratio = actual_burn_pct / expected_burn_pct if expected_burn_pct > 0 else 1.0

        if velocity_ratio < 0.70:
            status = 'CRITICAL_UNDERSPENDING'
            risk = 'Risk of fund lapsing or contractor mobilization delays'
        elif velocity_ratio > 1.25:
            status = 'OVERSPENDING_RISK'
            risk = 'High probability of budget overrun before fiscal year-end'
        else:
            status = 'HEALTHY_VELOCITY'
            risk = 'Disbursements on track with approved milestone schedule'

        return {
            'elapsed_months': m,
            'expected_burn_pct': round(Decimal(str(expected_burn_pct)), 1),
            'actual_burn_pct': round(Decimal(str(actual_burn_pct)), 1),
            'velocity_ratio': round(Decimal(str(velocity_ratio)), 2),
            'status': status,
            'risk_assessment': risk
        }
