import os
import pandas as pd
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from dashboard.models import MutualFundData
from django.conf import settings
import traceback

class Command(BaseCommand):
    help = "Fetch and update mutual fund data from CSV"

    def handle(self, *args, **kwargs):
        today = datetime.today().date()
        five_years_ago = today - timedelta(days=1825)

        # CSV path
        csv_path = os.path.join(settings.BASE_DIR, 'dashboard', 'static', 'csv', 'mutual_fund_data.csv')

        # Check if CSV file exists
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"❌ CSV file not found at: {csv_path}"))
            return

        # Read CSV
        try:
            mutual_fund_df = pd.read_csv(csv_path)
            mutual_fund_df.columns = mutual_fund_df.columns.str.strip()  # Column names ke spaces hata do
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading CSV: {e}"))
            return

        for _, row in mutual_fund_df.iterrows():
            try:
                scheme_code = str(row['Scheme Code']).strip()
                scheme_name = str(row['Scheme Name']).strip()
                isin_div_payout = str(row.get('ISIN Div Payout', '')).strip()
                isin_div_reinvestment = str(row.get('ISIN Div Reinvestment', '')).strip()
                net_asset_value = float(str(row['Net Asset Value']).replace(",", "").strip())
                date = pd.to_datetime(row['Date']).date()

                self.stdout.write(f"\n🔄 Updating data for {scheme_name} ({scheme_code}) on {date}...")

                # Save or update entry in MutualFundData model
                obj, created = MutualFundData.objects.update_or_create(
                    scheme_code=scheme_code,
                    date=date,
                    defaults={
                        'scheme_name': scheme_name,
                        'isin_div_payout': isin_div_payout,
                        'isin_div_reinvestment': isin_div_reinvestment,
                        'net_asset_value': net_asset_value,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Added new data for {scheme_name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"✅ Updated data for {scheme_name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to process row: {e}"))
                traceback.print_exc()

        # 🧹 Delete old records (older than 5 years)
        deleted, _ = MutualFundData.objects.filter(date__lt=five_years_ago).delete()
        self.stdout.write(self.style.SUCCESS(f"\n🧹 Old mutual fund records deleted: {deleted}"))

        self.stdout.write(self.style.SUCCESS("✅ Mutual Fund data update complete"))
        self.stdout.write(self.style.SUCCESS("All done! 🚀"))
