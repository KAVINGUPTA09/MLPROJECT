from flask import Flask, request, jsonify
import pandas as pd

from src.utils import load_artifacts, preprocess_live_input

app = Flask(__name__)

model, scaler, feature_columns, threshold = load_artifacts()


@app.route("/")
def home():
    return jsonify({
        "message": "Fraud Detection API Running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": True,
        "threshold": round(float(threshold), 2),
        "expected_input_columns": ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        processed = preprocess_live_input(data, scaler, feature_columns)

        prob = float(model.predict_proba(processed)[0][1])
        pred = 1 if prob >= threshold else 0

        result = {
            "fraud_prediction": int(pred),
            "fraud_probability": round(prob, 4),
            "threshold_used": round(float(threshold), 2),
            "risk_level": (
                "High" if prob >= 0.80 else
                "Medium" if prob >= 0.40 else
                "Low"
            )
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

        records = data["records"]

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
                    "fraud_prediction": int(pred),
                    "fraud_probability": round(prob, 4),
                    "threshold_used": round(float(threshold), 2),
                    "risk_level": (
                        "High" if prob >= 0.80 else
                        "Medium" if prob >= 0.40 else
                        "Low"
                    )
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
    app.run(debug=True)