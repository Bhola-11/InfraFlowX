"""
Management command to recalculate asset book value and replacement cost forecast.
"""
from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.assets.services import AssetService


class Command(BaseCommand):
    help = 'Recalculates straight-line depreciation and future replacement costs.'

    def handle(self, *args, **options):
        assets = Asset.objects.all()
        for a in assets:
            res = AssetService.recalculate_asset_book_value(a.id)
            self.stdout.write(f"  {a.asset_id}: Book Value ${res['current_value']:,} | Replacement Forecast ${res['forecast_replacement_cost']:,}")
        self.stdout.write(self.style.SUCCESS("Asset depreciation recalculation completed."))
