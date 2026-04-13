import json
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

from src.config import (
    DATA_PATH,
    MODEL_PATH,
    SCALER_PATH,
    FEATURE_COLUMNS_PATH,
    THRESHOLD_PATH,
    FEATURE_IMPORTANCE_PLOT,
    CONFUSION_MATRIX_PLOT,
    ROC_CURVE_PLOT,
    PR_CURVE_PLOT,
    SHAP_SUMMARY_PLOT
)
from src.preprocess import load_data, basic_cleaning, scale_columns, split_data
from src.feature_engineering import add_engineered_features
from src.evaluate import (
    find_best_threshold,
    evaluate_model,
    plot_confusion_matrix,
    plot_roc_curve,
    plot_pr_curve
)
from src.explain import generate_feature_importance, generate_shap_summary


# ---------------------------------------------------
# EXTRA PATHS FOR MULTI-MODEL SUPPORT
# ---------------------------------------------------
LOGISTIC_MODEL_PATH = "model/logistic.pkl"
RANDOM_FOREST_MODEL_PATH = "model/random_forest.pkl"
XGBOOST_MODEL_PATH = "model/xgboost.pkl"
MODEL_METRICS_PATH = "model/model_metrics.json"


# ---------------------------------------------------
# MODEL COMPARISON
# ---------------------------------------------------
def compare_models(X_train, y_train, X_test, y_test):
    models = {
        "logistic": LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        ),
        "xgboost": XGBClassifier(
            n_estimators=250,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42
        )
    }

    results = {}
    trained_models = {}
    thresholds = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)

        y_prob = model.predict_proba(X_test)[:, 1]
        threshold = find_best_threshold(y_test, y_prob)

        metrics, _, _, _ = evaluate_model(y_test, y_prob, threshold)

        # results[name] = {
        #     "accuracy": round(metrics["accuracy"], 4),
        #     "precision": round(metrics["precision"], 4),
        #     "recall": round(metrics["recall"], 4),
        #     "f1_score": round(metrics["f1_score"], 4),
        #     "roc_auc": round(metrics["roc_auc"], 4),
        #     "threshold": round(threshold, 4)
        # }
        results[name] = {
    "precision": round(metrics.get("precision", 0), 4),
    "recall": round(metrics.get("recall", 0), 4),
    "f1_score": round(metrics.get("f1_score", 0), 4),
    "roc_auc": round(metrics.get("roc_auc", 0), 4),
    "threshold": round(threshold, 4)
}

        trained_models[name] = model
        thresholds[name] = threshold

    comparison_df = pd.DataFrame(results).T.reset_index()
    comparison_df = comparison_df.rename(columns={"index": "model"})

    return comparison_df, trained_models, thresholds, results


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
def main():
    print("Loading dataset...")
    df = load_data(DATA_PATH)

    print("Cleaning dataset...")
    df = basic_cleaning(df)

    print("Adding engineered features...")
    df = add_engineered_features(df)

    print("Scaling Time and Amount...")
    df, scaler = scale_columns(df, ["Time", "Amount"])

    print("Splitting data...")
    X_train, X_test, y_train, y_test = split_data(df)

    feature_columns = X_train.columns.tolist()

    print("Applying SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    print("\nComparing models...")
    comparison_df, trained_models, thresholds, metrics_json = compare_models(
        X_train_resampled, y_train_resampled, X_test, y_test
    )

    print("\nModel Comparison:")
    print(comparison_df)

    # ---------------------------------------------------
    # SAVE ALL MODELS
    # ---------------------------------------------------
    print("\nSaving all trained models...")
    joblib.dump(trained_models["logistic"], LOGISTIC_MODEL_PATH)
    joblib.dump(trained_models["random_forest"], RANDOM_FOREST_MODEL_PATH)
    joblib.dump(trained_models["xgboost"], XGBOOST_MODEL_PATH)

    # Save old/default final model also for backward compatibility
    joblib.dump(trained_models["xgboost"], MODEL_PATH)

    # Save common artifacts
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(feature_columns, FEATURE_COLUMNS_PATH)

    # Save xgboost threshold as default threshold
    best_threshold = thresholds["xgboost"]
    joblib.dump(best_threshold, THRESHOLD_PATH)

    # Save comparison metrics for dashboard
    with open(MODEL_METRICS_PATH, "w") as f:
        json.dump(metrics_json, f, indent=4)

    # ---------------------------------------------------
    # FINAL XGBOOST REPORTS
    # ---------------------------------------------------
    print("\nGenerating final reports using XGBoost...")
    final_model = trained_models["xgboost"]

    y_prob = final_model.predict_proba(X_test)[:, 1]
    metrics, cm, report, _ = evaluate_model(y_test, y_prob, best_threshold)

    print("\nBest Threshold (XGBoost):", best_threshold)
    print("\nFinal Metrics (XGBoost):")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    print("\nClassification Report:")
    print(report)

    print("\nSaving plots...")
    plot_confusion_matrix(cm, CONFUSION_MATRIX_PLOT)
    plot_roc_curve(y_test, y_prob, ROC_CURVE_PLOT)
    plot_pr_curve(y_test, y_prob, PR_CURVE_PLOT)

    importance_df = generate_feature_importance(final_model, feature_columns, FEATURE_IMPORTANCE_PLOT)
    print("\nTop Features:")
    print(importance_df.head(15))

    print("Generating SHAP summary...")
    generate_shap_summary(final_model, X_test.iloc[:500], SHAP_SUMMARY_PLOT)

    print("\nTraining complete.")
    print("Saved:")
    print(f"- {LOGISTIC_MODEL_PATH}")
    print(f"- {RANDOM_FOREST_MODEL_PATH}")
    print(f"- {XGBOOST_MODEL_PATH}")
    print(f"- {SCALER_PATH}")
    print(f"- {FEATURE_COLUMNS_PATH}")
    print(f"- {THRESHOLD_PATH}")
    print(f"- {MODEL_METRICS_PATH}")
    print("Reports saved in 'report' folder.")


if __name__ == "__main__":
    main()