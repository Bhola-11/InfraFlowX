"""
Management command to run Markovian decay forecast simulation.
"""
from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.conditions.services import ConditionService


class Command(BaseCommand):
    help = 'Simulates 10-year Markov decay curves for infrastructure assets.'

    def handle(self, *args, **options):
        assets = Asset.objects.all()[:15]
        for a in assets:
            res = ConditionService.get_asset_deterioration_forecast(a, forecast_years=5)
            self.stdout.write(f"Asset {a.asset_id} ({a.asset_type}) Initial: {res['current_score']}")
            for yr_data in res['forecast']:
                self.stdout.write(f"  Year {yr_data['year']}: Expected Score {yr_data['expected_condition_score']} (State {yr_data['dominant_state']})")
        self.stdout.write(self.style.SUCCESS("Deterioration simulation completed."))
