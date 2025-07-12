import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from django.conf import settings
from dashboard.models import MutualFundData
import logging

logger = logging.getLogger(__name__)

def train_model_for_mutual_fund(scheme_name):
    try:
        # Fetch the data from the database
        queryset = MutualFundData.objects.filter(scheme_name=scheme_name).order_by('date').values('date', 'net_asset_value')

        # Check if data exists
        if not queryset.exists():
            logger.error(f"No data found for {scheme_name}")
            return f"No data for {scheme_name}"

        # Convert the queryset to a DataFrame
        df = pd.DataFrame(queryset)

        # Handle missing or invalid data
        df = df.dropna(subset=['net_asset_value', 'date'])

        # Convert 'date' to datetime and calculate the number of days
        df['date'] = pd.to_datetime(df['date'])
        df['days'] = (df['date'] - df['date'].min()).dt.days

        # Initialize and train the linear regression model
        model = LinearRegression()
        model.fit(df[['days']], df['net_asset_value'])

        # Define the directory to save the model
        model_dir = os.path.join(settings.BASE_DIR, 'ml', 'models', 'mutual_funds')
        os.makedirs(model_dir, exist_ok=True)

        # Make a safe file name
        safe_scheme_name = "".join(c for c in scheme_name if c.isalnum() or c in (' ', '_')).rstrip()
        model_path = os.path.join(model_dir, f'{safe_scheme_name}_model.pkl')

        # Save the trained model
        joblib.dump(model, model_path)

        logger.info(f"Model trained and saved for {scheme_name}")
        return f"✅ Trained and saved model for: {scheme_name}"

    except Exception as e:
        logger.error(f"Error while training model for {scheme_name}: {e}")
        return f"❌ Error while training model for {scheme_name}: {e}"
