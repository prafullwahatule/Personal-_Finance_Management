# ml/train_crypto_model.py

import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from django.conf import settings
from dashboard.models import CryptoHistoryData

def train_model_for_crypto(symbol):
    queryset = CryptoHistoryData.objects.filter(symbol=symbol).order_by('date').values('date', 'price_inr')
    if not queryset:
        return f"No data for {symbol}"

    df = pd.DataFrame(queryset)
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = (df['date'] - df['date'].min()).dt.days

    model = LinearRegression()
    model.fit(df[['days']], df['price_inr'])

    model_dir = os.path.join(settings.BASE_DIR, 'ml', 'models', 'crypto')
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, f'{symbol}_model.pkl')
    joblib.dump(model, model_path)

    return f"Trained and saved: {symbol}"
