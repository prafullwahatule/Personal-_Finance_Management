# ml/train_commodity_model.py
import os
import joblib
import pandas as pd
from django.conf import settings
from dashboard.models import CommodityData
from datetime import timedelta

# Convert time period like "7d", "1m", "3m", "1y" to number of days
def get_days_from_period(period):
    if period.endswith("d"):
        return int(period[:-1])
    elif period.endswith("m"):
        return int(period[:-1]) * 30
    elif period.endswith("y"):
        return int(period[:-1]) * 365
    return 0

def predict_price_for_commodity(name, period):
    model_path = os.path.join(settings.BASE_DIR, 'ml', 'models', 'commodity', f"{name}_model.pkl")

    if not os.path.exists(model_path):
        return f"Model for {name} not found"

    model = joblib.load(model_path)

    # Get latest date in DB
    data = CommodityData.objects.filter(name=name).order_by('-date')
    if not data.exists():
        return f"No data for {name}"

    last_date = data.first().date
    first_date = CommodityData.objects.filter(name=name).order_by('date').first().date
    days_passed = (last_date - first_date).days

    future_days = get_days_from_period(period)
    future_day_value = days_passed + future_days

    df_future = pd.DataFrame({'days': [future_day_value]})
    predicted_price = model.predict(df_future)[0]

    return round(predicted_price, 2)
