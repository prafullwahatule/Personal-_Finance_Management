# dashboard/management/commands/train_mutual_models.py

from django.core.management.base import BaseCommand
from ml.train_mutual_model import train_model_for_mutual_fund
from dashboard.models import MutualFundData
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Train models for all mutual funds from the database'

    def handle(self, *args, **options):
        # Fetch unique scheme names from the database
        unique_scheme_names = MutualFundData.objects.values_list('scheme_name', flat=True).distinct()

        for scheme_name in unique_scheme_names:
            try:
                self.stdout.write(f"🔁 Training model for: {scheme_name}")
                logger.info(f"Training model for: {scheme_name}")
                
                # Train the model for the scheme
                result = train_model_for_mutual_fund(scheme_name)

                self.stdout.write(result)
                logger.info(result)

            except Exception as e:
                error_message = f"❌ Failed to train model for {scheme_name}: {e}"
                self.stdout.write(error_message)
                logger.error(error_message)
