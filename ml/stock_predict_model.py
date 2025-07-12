
# ml/stock_predict_model.py

import os
import joblib
import pandas as pd
from django.conf import settings
from dashboard.models import StockData

def predict_price_for_symbol(symbol, days_ahead):
    model_path = os.path.join(settings.BASE_DIR, 'ml', 'models', 'stock', f'{symbol}_model.pkl')
    if not os.path.exists(model_path):
        return f"Model for {symbol} not found"

    model = joblib.load(model_path)

    last_date = StockData.objects.filter(symbol=symbol).order_by('-date').first().date
    first_date = StockData.objects.filter(symbol=symbol).order_by('date').first().date
    days_since_start = (last_date - first_date).days

    future_days = days_since_start + days_ahead

    # 🔥 FIX: Create DataFrame with correct column name
    future_df = pd.DataFrame({'days': [future_days]})
    future_price = model.predict(future_df)

    return float(round(future_price[0], 2))
