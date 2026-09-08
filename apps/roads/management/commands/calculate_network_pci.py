"""
Management command to recalculate PCI scores across all road corridors.
"""
from django.core.management.base import BaseCommand
from apps.roads.models import Road
from apps.roads.services import RoadService


class Command(BaseCommand):
    help = 'Recalculates ASTM D6433 Pavement Condition Index (PCI) for all road corridors.'

    def handle(self, *args, **options):
        roads = Road.objects.all()
        self.stdout.write(f"Evaluating {roads.count()} road networks...")
        updated = 0
        for road in roads:
            res = RoadService.evaluate_road_condition(road.id)
            self.stdout.write(f"  {road.road_code}: PCI {res['pci_score']} ({res['category']['rating']})")
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Successfully recalculated PCI for {updated} roads."))
