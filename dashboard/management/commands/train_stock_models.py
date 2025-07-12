# dashboard/management/commands/train_stock_models.py


from django.core.management.base import BaseCommand
from dashboard.models import StockData
from ml.stock_train_model import train_model_for_symbol

class Command(BaseCommand):
    help = "Train ML models for all stock symbols in DB"

    def handle(self, *args, **kwargs):
        symbols = StockData.objects.values_list('symbol', flat=True).distinct()
        for symbol in symbols:
            result = train_model_for_symbol(symbol)
            self.stdout.write(self.style.SUCCESS(result))







