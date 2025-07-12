# ml/predict_crypto_model.py

import os
import joblib
import pandas as pd
from django.conf import settings
from dashboard.models import CryptoHistoryData

def predict_price_for_crypto(symbol, days_ahead):
    model_path = os.path.join(settings.BASE_DIR, 'ml', 'models', 'crypto', f'{symbol}_model.pkl')
    if not os.path.exists(model_path):
        return f"Model for {symbol} not found"

    model = joblib.load(model_path)

    # Fetch the data for the given symbol
    first_date = CryptoHistoryData.objects.filter(symbol=symbol).order_by('date').first().date
    last_date = CryptoHistoryData.objects.filter(symbol=symbol).order_by('-date').first().date
    days_since_start = (last_date - first_date).days

    # Predict the future price by adding the days_ahead value
    future_days = days_since_start + days_ahead

    # Prepare the data for prediction
    future_df = pd.DataFrame({'days': [future_days]})
    future_price = model.predict(future_df)

    return float(round(future_price[0], 2))
