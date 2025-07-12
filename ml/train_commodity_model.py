# ml/train_commodity_model.py
import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from django.conf import settings
from dashboard.models import CommodityData
def train_model_for_commodity(name):
    print(f"Training model for: {name}")  # 👈 Debug print added here

    queryset = CommodityData.objects.filter(name=name).order_by('date').values('date', 'close')
    if not queryset:
        return f"No data for {name}"

    df = pd.DataFrame(queryset)
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = (df['date'] - df['date'].min()).dt.days  # Calculate days since the first date

    model = LinearRegression()
    model.fit(df[['days']], df['close'])

    model_dir = os.path.join(settings.BASE_DIR, 'ml', 'models', 'commodity')
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, f'{name}_model.pkl')
    joblib.dump(model, model_path)

    return f"Trained and saved: {name}"
