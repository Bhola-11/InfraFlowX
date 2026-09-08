"""
Conditions Domain Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.conditions.models import ConditionLog, DeteriorationModel
from apps.conditions.deterioration import MarkovDeteriorationEngine
from apps.audit.utils import log_audit_event


class ConditionService:
    @staticmethod
    def get_asset_deterioration_forecast(asset, forecast_years=10):
        # Map condition score to initial state index (0 to 4)
        score = asset.condition_score
        if score >= 90:
            init_idx = 0
        elif score >= 70:
            init_idx = 1
        elif score >= 50:
            init_idx = 2
        elif score >= 25:
            init_idx = 3
        else:
            init_idx = 4
            
        model = DeteriorationModel.objects.filter(asset_type=asset.asset_type).first()
        load_mult = model.heavy_load_multiplier if model else Decimal('1.0')
        clim_mult = model.severe_climate_multiplier if model else Decimal('1.0')
        
        forecast = MarkovDeteriorationEngine.forecast_decay_profile(
            asset_type=asset.asset_type,
            initial_state_idx=init_idx,
            years=forecast_years,
            load_multiplier=load_mult,
            climate_multiplier=clim_mult
        )
        return {
            'asset_id': asset.asset_id,
            'asset_type': asset.asset_type,
            'current_score': score,
            'forecast': forecast
        }

    @staticmethod
    @transaction.atomic
    def log_condition_assessment(asset, recorded_date, score, structural_idx, operational_idx, safety_idx, notes="", assessor=None):
        if score >= 90:
            cat = 'EXCELLENT'
        elif score >= 70:
            cat = 'GOOD'
        elif score >= 50:
            cat = 'FAIR'
        elif score >= 25:
            cat = 'POOR'
        else:
            cat = 'CRITICAL'
            
        clog = ConditionLog.objects.create(
            asset=asset,
            recorded_date=recorded_date,
            condition_score=score,
            condition_category=cat,
            structural_index=structural_idx,
            operational_index=operational_idx,
            safety_index=safety_idx,
            assessor=assessor,
            notes=notes
        )
        
        asset.condition = cat
        asset.condition_score = score
        asset.save(update_fields=['condition', 'condition_score'])
        
        log_audit_event(
            action='UPDATE',
            module='conditions',
            object_id=str(clog.id),
            object_repr=str(clog),
            description=f"Condition score {score}/100 logged for asset {asset.name}",
            user=assessor
        )
        return clog
