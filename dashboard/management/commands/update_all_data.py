from django.core.management.base import BaseCommand
from dashboard.management.commands.update_stock_data import Command as UpdateStockData
from dashboard.management.commands.update_commodity_data import Command as UpdateCommodityData
from dashboard.management.commands.update_mutual_fund import Command as UpdateMutualFundData
from dashboard.management.commands.update_crypto_data import Command as UpdateCryptoData

class Command(BaseCommand):
    help = 'Update all data modules'

    def handle(self, *args, **kwargs):
        print("🔄 Updating all data modules...\n")

        # Update Stock Data
        print("📈 Updating Stock Market Data...")
        UpdateStockData().handle()

        # Update Commodity Data
        print("\n🌾 Updating Commodity Data...")
        UpdateCommodityData().handle()

        # Update Mutual Fund / SIP Data
        print("\n💰 Updating Mutual Fund / SIP Data...")
        UpdateMutualFundData().handle()

        # Update Crypto Data
        print("\n🪙 Updating Cryptocurrency Data...")
        UpdateCryptoData().handle()

        self.stdout.write(self.style.SUCCESS("\n✅ All data updates completed successfully!"))
        print("🚀 All modules updated and ready.\n")
        print("🔄 Please check the database for updated records.")