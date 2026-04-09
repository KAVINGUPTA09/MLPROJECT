import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "creditcard.csv")

MODEL_DIR = os.path.join(BASE_DIR, "model")
REPORT_DIR = os.path.join(BASE_DIR, "report")

MODEL_PATH = os.path.join(MODEL_DIR, "fraud_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
FEATURE_COLUMNS_PATH = os.path.join(MODEL_DIR, "feature_columns.pkl")
THRESHOLD_PATH = os.path.join(MODEL_DIR, "threshold.pkl")

FEATURE_IMPORTANCE_PLOT = os.path.join(REPORT_DIR, "feature_importance.png")
CONFUSION_MATRIX_PLOT = os.path.join(REPORT_DIR, "confusion_matrix.png")
ROC_CURVE_PLOT = os.path.join(REPORT_DIR, "roc_curve.png")
PR_CURVE_PLOT = os.path.join(REPORT_DIR, "pr_curve.png")
SHAP_SUMMARY_PLOT = os.path.join(REPORT_DIR, "shap_summary.png")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)