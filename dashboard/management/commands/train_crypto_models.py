# dashboard/management/commands/train_crypto_models.py

from django.core.management.base import BaseCommand
from dashboard.models import CryptoHistoryData
from ml.train_crypto_model import train_model_for_crypto

class Command(BaseCommand):
    help = "Train ML models for all crypto symbols in DB"

    def handle(self, *args, **kwargs):
        symbols = CryptoHistoryData.objects.values_list('symbol', flat=True).distinct()
        for symbol in symbols:
            result = train_model_for_crypto(symbol)
            self.stdout.write(self.style.SUCCESS(result))
        self.stdout.write(self.style.SUCCESS("✅ All crypto models trained successfully!"))