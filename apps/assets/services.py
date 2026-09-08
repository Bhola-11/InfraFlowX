"""
Asset Enterprise Domain Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.assets.models import Asset, AssetCategory, AssetStatusHistory
from apps.assets.lifecycle import AssetDepreciationEngine
from apps.audit.utils import log_audit_event
from apps.notifications.utils import send_notification


class AssetService:
    @staticmethod
    def recalculate_asset_book_value(asset_id, inflation_rate=2.5):
        asset = Asset.objects.get(id=asset_id)
        today = timezone.now().date()
        age_years = (today - asset.installation_date).days // 365 if asset.installation_date else 0
        
        dep_result = AssetDepreciationEngine.calculate_straight_line_depreciation(
            cost=asset.acquisition_cost,
            salvage_value=asset.acquisition_cost * Decimal('0.05'),
            useful_life_years=asset.useful_life_years,
            age_years=age_years
        )
        
        asset.current_value = dep_result['current_book_value']
        asset.save(update_fields=['current_value'])
        
        forecast_rep = AssetDepreciationEngine.forecast_replacement_cost(
            current_cost=asset.acquisition_cost,
            inflation_rate_pct=inflation_rate,
            years_until_replacement=dep_result['remaining_useful_life']
        )
        
        return {
            'asset_id': asset.asset_id,
            'name': asset.name,
            'acquisition_cost': asset.acquisition_cost,
            'current_value': asset.current_value,
            'depreciation_summary': dep_result,
            'forecast_replacement_cost': forecast_rep
        }

    @staticmethod
    @transaction.atomic
    def transition_asset_status(asset, new_status, reason="", changed_by=None):
        old_status = asset.status
        if old_status == new_status:
            return asset
            
        asset.status = new_status
        asset.save(update_fields=['status'])
        
        AssetStatusHistory.objects.create(
            asset=asset,
            previous_status=old_status,
            new_status=new_status,
            reason=reason,
            changed_by=changed_by
        )
        
        log_audit_event(
            action='ASSET_CHANGE',
            module='assets',
            object_id=str(asset.id),
            object_repr=str(asset),
            changes={'status': {'from': old_status, 'to': new_status}},
            description=f"Status changed from {old_status} to {new_status}. Reason: {reason}",
            user=changed_by
        )
        
        if new_status in ['DAMAGED', 'DISPOSED'] and changed_by:
            send_notification(
                recipient=changed_by,
                title=f"Asset Status Alert: {asset.asset_id}",
                message=f"Asset '{asset.name}' was transitioned to status {new_status}.",
                notification_type='WARNING',
                priority='HIGH'
            )
            
        return asset
