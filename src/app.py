# import os
# from flask import Flask, request, jsonify
# import pandas as pd

# # ── Path setup (fixes model loading on Render) ──────────────────────────────
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "model")

# from src.utils import load_artifacts, preprocess_live_input

# app = Flask(__name__)

# # Pass MODEL_DIR into load_artifacts so it knows where to find .pkl files
# model, scaler, feature_columns, threshold = load_artifacts(MODEL_DIR)


# @app.route("/")
# def home():
#     return jsonify({
#         "message": "Fraud Detection API Running"
#     })


# @app.route("/health")
# def health():
#     return jsonify({
#         "status": "ok",
#         "model_loaded": True,
#         "threshold": round(float(threshold), 2),
#         "expected_input_columns": ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
#     })


# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.get_json()

#         if data is None:
#             return jsonify({"error": "No JSON data received"}), 400

#         processed = preprocess_live_input(data, scaler, feature_columns)

#         prob = float(model.predict_proba(processed)[0][1])
#         pred = 1 if prob >= threshold else 0

#         result = {
#             "fraud_prediction": int(pred),
#             "fraud_probability": round(prob, 4),
#             "threshold_used": round(float(threshold), 2),
#             "risk_level": (
#                 "High" if prob >= 0.80 else
#                 "Medium" if prob >= 0.40 else
#                 "Low"
#             )
#         }

#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


# @app.route("/predict_batch", methods=["POST"])
# def predict_batch():
#     try:
#         data = request.get_json()

#         if data is None or "records" not in data:
#             return jsonify({"error": "Expected JSON with key 'records'"}), 400

#         records = data["records"]

#         if not isinstance(records, list) or len(records) == 0:
#             return jsonify({"error": "Records must be a non-empty list"}), 400

#         results = []
#         row_errors = []

#         for idx, record in enumerate(records):
#             try:
#                 processed = preprocess_live_input(record, scaler, feature_columns)
#                 prob = float(model.predict_proba(processed)[0][1])
#                 pred = 1 if prob >= threshold else 0

#                 results.append({
#                     "row_index": idx,
#                     "fraud_prediction": int(pred),
#                     "fraud_probability": round(prob, 4),
#                     "threshold_used": round(float(threshold), 2),
#                     "risk_level": (
#                         "High" if prob >= 0.80 else
#                         "Medium" if prob >= 0.40 else
#                         "Low"
#                     )
#                 })

#             except Exception as row_error:
#                 row_errors.append({
#                     "row_index": idx,
#                     "error": str(row_error)
#                 })

#         return jsonify({
#             "results": results,
#             "row_errors": row_errors,
#             "processed_rows": len(results),
#             "failed_rows": len(row_errors)
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=False)
import os
import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify

from src.utils import preprocess_live_input

# ── Path setup (Render-safe) ──────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

app = Flask(__name__)

# ---------------------------------------------------------
# LOAD COMMON ARTIFACTS
# ---------------------------------------------------------
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))

# threshold optional
threshold_path = os.path.join(MODEL_DIR, "threshold.pkl")
if os.path.exists(threshold_path):
    threshold = joblib.load(threshold_path)
else:
    threshold = 0.5

# ---------------------------------------------------------
# LOAD MULTIPLE MODELS
# ---------------------------------------------------------
models = {}

model_files = {
    "logistic": "logistic.pkl",
    "random_forest": "random_forest.pkl",
    "xgboost": "xgboost.pkl"
}

for model_name, file_name in model_files.items():
    file_path = os.path.join(MODEL_DIR, file_name)
    if os.path.exists(file_path):
        models[model_name] = joblib.load(file_path)

# fallback for old single-model project
old_model_path = os.path.join(MODEL_DIR, "fraud_model.pkl")
if "xgboost" not in models and os.path.exists(old_model_path):
    models["xgboost"] = joblib.load(old_model_path)

# ---------------------------------------------------------
# LOAD MODEL METRICS (optional)
# ---------------------------------------------------------
metrics_path = os.path.join(MODEL_DIR, "model_metrics.json")
if os.path.exists(metrics_path):
    with open(metrics_path, "r") as f:
        model_metrics = json.load(f)
else:
    model_metrics = {}

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def get_risk_level(prob: float) -> str:
    if prob >= 0.80:
        return "High"
    elif prob >= 0.40:
        return "Medium"
    return "Low"

def get_model(model_name: str):
    if model_name in models:
        return models[model_name]
    return models.get("xgboost", None)


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Fraud Detection API Running",
        "available_models": list(models.keys())
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": len(models) > 0,
        "available_models": list(models.keys()),
        "threshold": round(float(threshold), 2),
        "expected_input_columns": ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
    })


# @app.route("/metrics", methods=["GET"])
# def metrics():
#     return jsonify(model_metrics)
@app.route("/metrics", methods=["GET"])
def metrics():
    try:
        metrics_path = os.path.join(MODEL_DIR, "model_metrics.json")

        if not os.path.exists(metrics_path):
            return jsonify({"error": "model_metrics.json not found"}), 404

        with open(metrics_path, "r") as f:
            metrics_data = json.load(f)

        return jsonify(metrics_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        # model selection from UI
        model_name = data.get("model", "xgboost")

        # remove model key from actual input
        input_data = {k: v for k, v in data.items() if k != "model"}

        model = get_model(model_name)
        if model is None:
            return jsonify({"error": f"Model '{model_name}' not found"}), 400

        processed = preprocess_live_input(input_data, scaler, feature_columns)

        prob = float(model.predict_proba(processed)[0][1])
        pred = 1 if prob >= threshold else 0

        result = {
            "model_used": model_name,
            "fraud_prediction": int(pred),
            "fraud_probability": round(prob, 4),
            "threshold_used": round(float(threshold), 2),
            "risk_level": get_risk_level(prob)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    try:
        data = request.get_json()

        if data is None or "records" not in data:
            return jsonify({"error": "Expected JSON with key 'records'"}), 400

        model_name = data.get("model", "xgboost")
        records = data["records"]

        model = get_model(model_name)
        if model is None:
            return jsonify({"error": f"Model '{model_name}' not found"}), 400

        if not isinstance(records, list) or len(records) == 0:
            return jsonify({"error": "Records must be a non-empty list"}), 400

        results = []
        row_errors = []

        for idx, record in enumerate(records):
            try:
                processed = preprocess_live_input(record, scaler, feature_columns)

                prob = float(model.predict_proba(processed)[0][1])
                pred = 1 if prob >= threshold else 0

                results.append({
                    "row_index": idx,
                    "model_used": model_name,
                    "fraud_prediction": int(pred),
                    "fraud_probability": round(prob, 4),
                    "threshold_used": round(float(threshold), 2),
                    "risk_level": get_risk_level(prob)
                })

            except Exception as row_error:
                row_errors.append({
                    "row_index": idx,
                    "error": str(row_error)
                })

        return jsonify({
            "results": results,
            "row_errors": row_errors,
            "processed_rows": len(results),
            "failed_rows": len(row_errors)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)