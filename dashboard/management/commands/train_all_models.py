from django.core.management.base import BaseCommand
from dashboard.management.commands.train_stock_models import Command as TrainStockModels
from dashboard.management.commands.train_mutual_models import Command as TrainMutualFundModels
from dashboard.management.commands.train_commodity_models import Command as TrainCommodityModels
from dashboard.management.commands.train_crypto_models import Command as TrainCryptoModels
import logging

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Train ML models for all financial instruments (stocks + mutual funds + commodities)'

    def handle(self, *args, **kwargs):
        self.stdout.write("⚙️ Starting full model training...\n")
        logger.info("Starting full model training...")

        try:
            # Train mutual fund models
            self.stdout.write("💰 Training Mutual Fund Models...")
            logger.info("Training Mutual Fund Models...")
            TrainMutualFundModels().handle()

            # Train stock models
            self.stdout.write("\n📈 Training Stock Models...")
            logger.info("Training Stock Models...")
            TrainStockModels().handle()

            # Train commodity models
            self.stdout.write("\n🌾 Training Commodity Models...")
            logger.info("Training Commodity Models...")
            TrainCommodityModels().handle()

            # Train crypto models
            self.stdout.write("\n💎 Training Crypto Models...")
            logger.info("Training Crypto Models...")
            TrainCryptoModels().handle()

            self.stdout.write(self.style.SUCCESS("\n✅ All models trained successfully!"))
            logger.info("All models trained successfully!")
            print("🚀 All training modules completed.\n")

        except Exception as e:
            error_message = f"❌ An error occurred during model training: {e}"
            self.stdout.write(self.style.ERROR(error_message))
            logger.error(error_message)
            print("❌ An error occurred during model training.")    