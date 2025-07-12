
# dashboard/management/commands/train_commodity_models.py
from django.core.management.base import BaseCommand
from ml.train_commodity_model import train_model_for_commodity
from dashboard.models import CommodityData

class Command(BaseCommand):
    help = "Train commodity models"

    def handle(self, *args, **kwargs):
        commodities = CommodityData.objects.values_list('name', flat=True).distinct()

        for name in commodities:
            result = train_model_for_commodity(name)
            self.stdout.write(self.style.SUCCESS(result))
