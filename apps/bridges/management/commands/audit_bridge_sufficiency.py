"""
Management command to recalculate FHWA Sufficiency Ratings across all bridges.
"""
from django.core.management.base import BaseCommand
from apps.bridges.models import Bridge
from apps.bridges.services import BridgeService


class Command(BaseCommand):
    help = 'Audits FHWA Bridge Sufficiency Ratings (SR) and federal funding eligibility.'

    def handle(self, *args, **options):
        bridges = Bridge.objects.all()
        self.stdout.write(f"Auditing {bridges.count()} bridge structures...")
        for brg in bridges:
            res = BridgeService.perform_structural_audit(brg.id)
            self.stdout.write(f"  {brg.bridge_id_code}: SR {res['sufficiency_rating']}% [{res['condition']}] - {res['eligibility']['status']}")
        self.stdout.write(self.style.SUCCESS("Bridge structural audit completed successfully."))
