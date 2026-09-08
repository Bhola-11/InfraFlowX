"""
Management command to compute MTBF / MTTR equipment metrics.
"""
from django.core.management.base import BaseCommand
from apps.facilities.models import FacilityEquipment
from apps.facilities.services import FacilityService


class Command(BaseCommand):
    help = 'Computes MTBF, MTTR and availability across facility equipment.'

    def handle(self, *args, **options):
        equipment = FacilityEquipment.objects.all()
        for eq in equipment:
            res = FacilityService.compute_equipment_health(eq.id)
            m = res['metrics']
            self.stdout.write(f"  {eq.equipment_code}: Availability {m['availability_pct']}% | MTBF {m['mtbf_hours']}h | MTTR {m['mttr_hours']}h")
        self.stdout.write(self.style.SUCCESS("Equipment reliability calculation completed."))
