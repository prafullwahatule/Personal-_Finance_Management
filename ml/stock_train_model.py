# ml/stock_train_model.py

import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from django.conf import settings
from dashboard.models import StockData

def train_model_for_symbol(symbol):
    queryset = StockData.objects.filter(symbol=symbol).order_by('date').values('date', 'close')
    if not queryset:
        return f"No data for {symbol}"

    df = pd.DataFrame(queryset)
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = (df['date'] - df['date'].min()).dt.days

    model = LinearRegression()
    model.fit(df[['days']], df['close'])

    model_dir = os.path.join(settings.BASE_DIR, 'ml', 'models','stock')
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, f'{symbol}_model.pkl')
    joblib.dump(model, model_path)

    return f"Trained and saved: {symbol}"
