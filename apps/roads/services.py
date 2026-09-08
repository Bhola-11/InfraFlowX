"""
Road & Highway Domain Services
Business workflows for road network management, defect triage,
repair cost budgeting, and condition indexing.
"""
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.roads.models import Road, RoadDefect, RoadRepairHistory
from apps.roads.engineering import PavementConditionEngine, AASHTODesignEngine
from apps.audit.utils import log_audit_event
from apps.notifications.utils import send_notification


class RoadService:
    @staticmethod
    def evaluate_road_condition(road_id):
        """
        Re-calculates PCI and logs assessment.
        """
        road = Road.objects.select_related('asset').prefetch_related('defects').get(id=road_id)
        active_defects = [
            {
                'defect_type': d.defect_type,
                'severity': d.severity,
                'area_sqm': 4.5
            }
            for d in road.defects.filter(is_repaired=False)
        ]
        
        calculated_pci = PavementConditionEngine.calculate_pci(
            road_length_km=road.length_km,
            road_width_m=road.width_meters,
            defects=active_defects
        )
        
        road.pci_score = calculated_pci
        road.save(update_fields=['pci_score'])
        
        if road.asset:
            road.asset.condition_score = calculated_pci
            cat_info = PavementConditionEngine.get_pci_category(calculated_pci)
            road.asset.condition = cat_info['rating'] if cat_info['rating'] in ['GOOD', 'FAIR', 'POOR', 'EXCELLENT', 'CRITICAL'] else 'FAIR'
            road.asset.save(update_fields=['condition_score', 'condition'])
            
        return {
            'road_code': road.road_code,
            'pci_score': calculated_pci,
            'category': PavementConditionEngine.get_pci_category(calculated_pci),
            'active_defects_count': len(active_defects)
        }

    @staticmethod
    @transaction.atomic
    def report_defect(road, defect_type, severity, chainage_km, description, photo=None, user=None):
        """
        Registers a new field defect and dispatches notifications if critical.
        """
        defect = RoadDefect.objects.create(
            road=road,
            defect_type=defect_type,
            severity=severity,
            chainage_km=chainage_km,
            description=description,
            photo=photo
        )
        
        RoadService.evaluate_road_condition(road.id)
        
        log_audit_event(
            action='CREATE',
            module='roads',
            object_id=str(defect.id),
            object_repr=str(defect),
            description=f"Defect {defect_type} logged at KM {chainage_km} on {road.road_code}",
            user=user
        )
        
        if severity in ['HIGH', 'CRITICAL'] and user:
            send_notification(
                recipient=user,
                title=f"Critical Road Hazard: {road.road_code}",
                message=f"Defect {defect.get_defect_type_display()} reported at KM {chainage_km}. Immediate dispatch required.",
                notification_type='EMERGENCY',
                priority='HIGH'
            )
            
        return defect

    @staticmethod
    @transaction.atomic
    def record_repair_completion(road, repair_title, repair_type, cost, contractor_name, completion_date, pci_gain, summary="", user=None):
        """
        Logs paving repair and closes matching defects.
        """
        repair = RoadRepairHistory.objects.create(
            road=road,
            repair_title=repair_title,
            repair_type=repair_type,
            cost=cost,
            contractor_name=contractor_name,
            completion_date=completion_date,
            pci_gain=pci_gain,
            summary=summary
        )
        
        # Mark local defects as repaired
        road.defects.filter(is_repaired=False).update(is_repaired=True)
        road.pci_score = min(100, road.pci_score + pci_gain)
        road.last_resurfaced_date = completion_date
        road.save(update_fields=['pci_score', 'last_resurfaced_date'])
        
        if road.asset:
            road.asset.condition_score = road.pci_score
            road.asset.save(update_fields=['condition_score'])
            
        log_audit_event(
            action='MAINTENANCE_ACTION',
            module='roads',
            object_id=str(repair.id),
            object_repr=str(repair),
            description=f"Repair '{repair_title}' completed on {road.road_code}. Cost: ${cost:,}",
            user=user
        )
        return repair
