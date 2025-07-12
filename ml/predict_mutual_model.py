import os
import joblib
import pandas as pd
from django.conf import settings
from dashboard.models import MutualFundData
import logging

logger = logging.getLogger(__name__)

def predict_nav_for_mutual_fund(scheme_name, days_ahead):
    try:
        # Make a safe file name
        safe_scheme_name = "".join(c for c in scheme_name if c.isalnum() or c in (' ', '_')).rstrip()
        model_path = os.path.join(settings.BASE_DIR, 'ml', 'models', 'mutual_funds', f'{safe_scheme_name}_model.pkl')

        # Check if model file exists
        if not os.path.exists(model_path):
            logger.error(f"Model for {scheme_name} not found")
            return f"Model for {scheme_name} not found"

        # Load the trained model
        model = joblib.load(model_path)

        # Get the most recent and earliest NAV data for the fund
        last_record = MutualFundData.objects.filter(scheme_name=scheme_name).order_by('-date').first()
        first_record = MutualFundData.objects.filter(scheme_name=scheme_name).order_by('date').first()

        if not last_record or not first_record:
            logger.error(f"No data found for {scheme_name}")
            return f"No data found for {scheme_name}"

        # Calculate the number of days since the earliest data point
        days_since_start = (last_record.date - first_record.date).days

        # Predict the NAV for the given number of days ahead
        future_days = days_since_start + days_ahead
        future_df = pd.DataFrame({'days': [future_days]})
        future_nav = model.predict(future_df)

        predicted_nav = round(future_nav[0], 2)
        logger.info(f"Prediction for {scheme_name} in {days_ahead} days: {predicted_nav}")
        return predicted_nav

    except Exception as e:
        logger.error(f"Error while predicting NAV for {scheme_name}: {e}")
        return f"Error while predicting NAV for {scheme_name}: {e}"
