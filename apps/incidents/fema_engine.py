"""
FEMA Public Assistance (PA) Disaster Damage & Cost Recovery Engine
Implements federal disaster grant cost-share calculations (75% Federal, 25% State/Municipal).
"""
from decimal import Decimal


class FEMADisasterRecoveryEngine:
    @staticmethod
    def calculate_disaster_cost_share(emergency_debris_removal_cost, emergency_protective_measures_cost, permanent_infrastructure_restoration_cost, federal_cost_share_pct=75.0):
        c_debris = Decimal(str(emergency_debris_removal_cost))
        c_protective = Decimal(str(emergency_protective_measures_cost))
        c_perm = Decimal(str(permanent_infrastructure_restoration_cost))

        total_eligible = c_debris + c_protective + c_perm
        fed_rate = Decimal(str(federal_cost_share_pct)) / Decimal('100.0')

        federal_reimbursement = total_eligible * fed_rate
        local_cost_share = total_eligible - federal_reimbursement

        return {
            'debris_removal_cost': c_debris,
            'emergency_measures_cost': c_protective,
            'permanent_restoration_cost': c_perm,
            'total_eligible_damage_cost': total_eligible,
            'federal_grant_reimbursement': round(federal_reimbursement, 2),
            'municipal_local_share': round(local_cost_share, 2),
            'federal_share_rate_pct': Decimal(str(federal_cost_share_pct))
        }
