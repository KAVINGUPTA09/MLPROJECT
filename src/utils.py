import joblib
import pandas as pd
import os
from src.feature_engineering import add_engineered_features
# ✅ Removed unused: from src.config import MODEL_PATH, SCALER_PATH, etc.


def load_artifacts(model_dir):
    model     = joblib.load(os.path.join(model_dir, "fraud_model.pkl"))
    scaler    = joblib.load(os.path.join(model_dir, "scaler.pkl"))
    features  = joblib.load(os.path.join(model_dir, "feature_columns.pkl"))
    threshold = joblib.load(os.path.join(model_dir, "threshold.pkl"))
    return model, scaler, features, threshold


def preprocess_live_input(input_data, scaler, feature_columns):
    df = pd.DataFrame([input_data])

    df = add_engineered_features(df)

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.fillna(0)

    scale_cols = [col for col in ["Time", "Amount"] if col in df.columns]
    if len(scale_cols) == 2:
        df[["Time", "Amount"]] = scaler.transform(df[["Time", "Amount"]])

    return df