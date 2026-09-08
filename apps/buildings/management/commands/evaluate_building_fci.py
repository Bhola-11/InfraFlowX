"""
Management command to compute Facility Condition Index (FCI) for all municipal buildings.
"""
from django.core.management.base import BaseCommand
from apps.buildings.models import Building
from apps.buildings.services import BuildingService


class Command(BaseCommand):
    help = 'Computes Facility Condition Index (FCI) across all public buildings.'

    def handle(self, *args, **options):
        buildings = Building.objects.all()
        for b in buildings:
            res = BuildingService.evaluate_building_fci(b.id)
            self.stdout.write(f"  {b.building_id_code}: FCI {res['fci_score']} [{res['fci_status']['status']}]")
        self.stdout.write(self.style.SUCCESS("Building FCI evaluation completed."))
