import os
import pandas as pd
import cryptocompare
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from dashboard.models import CryptoHistoryData
from django.conf import settings
import traceback

class Command(BaseCommand):
    help = "Fetch and update daily cryptocurrency data using CryptoCompare"

    def handle(self, *args, **kwargs):
        today = datetime.today().date()
        five_years_ago = today - timedelta(days=1825)

        # CSV path
        csv_path = os.path.join(settings.BASE_DIR, 'dashboard', 'static', 'csv', 'crypto_symbols.csv')
        crypto_df = pd.read_csv(csv_path)  # CSV must have columns: Name, Symbol

        # Set your API key
        cryptocompare.cryptocompare._set_api_key_parameter('be44fbec2026a57f9cb9e8676e9d2d2f023da8d29902a4d3d8e3d1aaa5fed0ca')

        for _, row in crypto_df.iterrows():
            name = row['Name']
            symbol = row['Symbol']

            self.stdout.write(f"\n🔄 Updating data for {name} ({symbol})...")

            try:
                historical_data = cryptocompare.get_historical_price_day(
                    symbol, currency='INR', toTs=datetime.now(), limit=1825
                )

                if not historical_data:
                    self.stdout.write(self.style.WARNING(f"⚠️ No data found for {symbol}. Skipping."))
                    continue

                # Process historical data
                for data in historical_data:
                    date = datetime.utcfromtimestamp(data.get('time')).date()

                    if date >= five_years_ago:
                        open_value = float(data.get('open', 0) or 0)
                        close_value = float(data.get('close', 0) or 0)
                        volume_value = float(data.get('volumefrom', 0) or 0)

                        change_24h = 0
                        if open_value != 0:
                            change_24h = (close_value - open_value) / open_value * 100

                        # Save or update entry in CryptoHistoryData model
                        obj, created = CryptoHistoryData.objects.update_or_create(
                            name=name,
                            symbol=symbol,
                            date=date,
                            defaults={
                                'price_inr': close_value,
                                'market_cap_inr': close_value * volume_value,
                                'volume_24h': volume_value,
                                'change_24h': change_24h,
                            }
                        )

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"❌ Failed to fetch data for {symbol}: {e}"
                ))
                traceback.print_exc()

        # 🧹 Delete old records (older than 5 years)
        deleted, _ = CryptoHistoryData.objects.filter(date__lt=five_years_ago).delete()
        self.stdout.write(self.style.SUCCESS(f"\n🧹 Old crypto records deleted: {deleted}"))

        self.stdout.write(self.style.SUCCESS("✅ Crypto Live + Historical data update complete"))
        self.stdout.write(self.style.SUCCESS(f"\nOld records deleted: {deleted}"))
        self.stdout.write(self.style.SUCCESS("Update complete ✅"))
        self.stdout.write(self.style.SUCCESS("Data updated successfully!"))
        self.stdout.write(self.style.SUCCESS("All done! 🚀"))

        