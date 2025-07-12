import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from dashboard.models import StockData
from django.conf import settings

class Command(BaseCommand):
    help = "Fetch and update daily stock data"

    def handle(self, *args, **kwargs):
        today = datetime.today().date()
        five_years_ago = today - timedelta(days=1825)

        # CSV path
        csv_path = os.path.join(settings.BASE_DIR, 'dashboard', 'static', 'csv', 'nifty_50_stocks.csv')
        stocks_df = pd.read_csv(csv_path)
        stock_symbols = stocks_df['Symbol'].tolist()

        for symbol in stock_symbols:
            self.stdout.write(f"\nUpdating data for {symbol}...")
            try:
                # data = yf.download(symbol, period="5y", interval="1d")
                data = yf.download(symbol, period="5y", interval="1d", auto_adjust=True)
                if data.empty:
                    self.stdout.write(self.style.WARNING(f"No data found for {symbol}. Skipping."))
                    continue

                data.reset_index(inplace=True)

                for index, row in data.iterrows():
                    try:
                        # Extract the date correctly (row['Date'] might be a Series)
                        date_value = row['Date']
                        if isinstance(date_value, pd.Series):
                            date_value = date_value.iloc[0]  # Get the first element of the Series

                        # Ensure the date is a datetime object
                        date = pd.to_datetime(date_value).date()

                        # Get the stock data values with .iloc[0] for Series objects
                        open_value = float(row['Open'].iloc[0]) if isinstance(row['Open'], pd.Series) else float(row['Open'])
                        high_value = float(row['High'].iloc[0]) if isinstance(row['High'], pd.Series) else float(row['High'])
                        low_value = float(row['Low'].iloc[0]) if isinstance(row['Low'], pd.Series) else float(row['Low'])
                        close_value = float(row['Close'].iloc[0]) if isinstance(row['Close'], pd.Series) else float(row['Close'])
                        volume_value = int(row['Volume'].iloc[0]) if isinstance(row['Volume'], pd.Series) else int(row['Volume'])

                        # Check if the date is within the last 5 years
                        if date >= five_years_ago:
                            StockData.objects.get_or_create(
                                date=date,
                                symbol=symbol,
                                defaults={
                                    'open': open_value,
                                    'high': high_value,
                                    'low': low_value,
                                    'close': close_value,
                                    'volume': volume_value,
                                }
                            )
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Skipped row for {symbol} on {row['Date']} due to error: {e}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to fetch data for {symbol}: {e}"))

        # Delete old data (> 5 years)
        deleted, _ = StockData.objects.filter(date__lt=five_years_ago).delete()
        self.stdout.write(self.style.SUCCESS(f"\nOld records deleted: {deleted}"))
        self.stdout.write(self.style.SUCCESS("Update complete ✅"))
        self.stdout.write(self.style.SUCCESS("Data updated successfully!"))
        self.stdout.write(self.style.SUCCESS("All done! 🚀"))












