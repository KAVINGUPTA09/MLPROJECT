import joblib
import pandas as pd

from src.config import MODEL_PATH, SCALER_PATH, FEATURE_COLUMNS_PATH, THRESHOLD_PATH
from src.feature_engineering import add_engineered_features


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
    threshold = joblib.load(THRESHOLD_PATH)
    return model, scaler, feature_columns, threshold


def preprocess_live_input(input_data, scaler, feature_columns):
    df = pd.DataFrame([input_data])

    # Add engineered features exactly like training
    df = add_engineered_features(df)

    # Ensure all required columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Keep only training columns
    df = df[feature_columns]

    # Convert all values to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill NaN after conversion
    df = df.fillna(0)

    # Scale Time and Amount
    scale_cols = [col for col in ["Time", "Amount"] if col in df.columns]
    if len(scale_cols) == 2:
        df[["Time", "Amount"]] = scaler.transform(df[["Time", "Amount"]])

    return df