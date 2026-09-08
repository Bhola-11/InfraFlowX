"""
Bridge Management Services
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.bridges.models import Bridge, BridgeComponentInspection
from apps.bridges.engineering import BridgeSufficiencyEngine, BridgeScourEngine
from apps.audit.utils import log_audit_event
from apps.notifications.utils import send_notification


class BridgeService:
    @staticmethod
    def perform_structural_audit(bridge_id):
        bridge = Bridge.objects.prefetch_related('components').get(id=bridge_id)
        components = list(bridge.components.all())
        
        deck = next((c.rating_score_1_to_9 for c in components if c.component == 'DECK'), 7)
        super_str = next((c.rating_score_1_to_9 for c in components if c.component == 'SUPERSTRUCTURE'), 7)
        sub_str = next((c.rating_score_1_to_9 for c in components if c.component == 'SUBSTRUCTURE'), 7)
        
        sr = BridgeSufficiencyEngine.calculate_sufficiency_rating(
            bridge=bridge,
            deck_rating=deck,
            super_rating=super_str,
            sub_rating=sub_str,
        )
        
        # Determine overall condition
        min_r = min(deck, super_str, sub_str)
        if min_r >= 8:
            cond = 'EXCELLENT'
        elif min_r >= 7:
            cond = 'GOOD'
        elif min_r >= 5:
            cond = 'FAIR'
        elif min_r >= 4:
            cond = 'POOR'
        else:
            cond = 'CRITICAL'
            
        bridge.condition = cond
        bridge.save(update_fields=['condition'])
        
        if bridge.asset:
            bridge.asset.condition = cond
            bridge.asset.condition_score = int(round(float(sr)))
            bridge.asset.save(update_fields=['condition', 'condition_score'])
            
        return {
            'bridge_code': bridge.bridge_id_code,
            'sufficiency_rating': sr,
            'condition': cond,
            'eligibility': BridgeSufficiencyEngine.get_federal_eligibility(sr),
            'components_audited': len(components)
        }

    @staticmethod
    @transaction.atomic
    def record_component_rating(bridge, component, rating_score, findings="", photo=None, inspected_date=None, user=None):
        inspected_date = inspected_date or timezone.now().date()
        rec = BridgeComponentInspection.objects.create(
            bridge=bridge,
            component=component,
            rating_score_1_to_9=rating_score,
            findings=findings,
            photo=photo,
            inspected_date=inspected_date
        )
        
        BridgeService.perform_structural_audit(bridge.id)
        
        log_audit_event(
            action='UPDATE',
            module='bridges',
            object_id=str(rec.id),
            object_repr=str(rec),
            description=f"Component {component} rated {rating_score}/9 on Bridge {bridge.bridge_id_code}",
            user=user
        )
        
        if rating_score <= 4 and user:
            send_notification(
                recipient=user,
                title=f"Critical Structural Alert: {bridge.bridge_id_code}",
                message=f"Bridge component {rec.get_component_display()} received critical rating {rating_score}/9. Immediate engineering review triggered.",
                notification_type='EMERGENCY',
                priority='CRITICAL'
            )
            
        return rec
