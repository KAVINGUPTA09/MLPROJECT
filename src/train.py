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


def compare_models(X_train, y_train, X_test, y_test):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=250,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42
        )
    }

    results = []

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_prob = model.predict_proba(X_test)[:, 1]
        threshold = find_best_threshold(y_test, y_prob)
        metrics, _, _, _ = evaluate_model(y_test, y_prob, threshold)

        results.append({
            "Model": name,
            "Precision": round(metrics["precision"], 4),
            "Recall": round(metrics["recall"], 4),
            "F1": round(metrics["f1_score"], 4),
            "ROC_AUC": round(metrics["roc_auc"], 4),
            "Threshold": round(threshold, 2)
        })

    return pd.DataFrame(results)


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
    comparison_df = compare_models(X_train_resampled, y_train_resampled, X_test, y_test)
    print("\nModel Comparison:")
    print(comparison_df)

    print("\nTraining final XGBoost model...")
    model = XGBClassifier(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train_resampled, y_train_resampled)

    y_prob = model.predict_proba(X_test)[:, 1]
    best_threshold = find_best_threshold(y_test, y_prob)

    metrics, cm, report, _ = evaluate_model(y_test, y_prob, best_threshold)

    print("\nBest Threshold:", best_threshold)
    print("\nFinal Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    print("\nClassification Report:")
    print(report)

    print("\nSaving model files...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(feature_columns, FEATURE_COLUMNS_PATH)
    joblib.dump(best_threshold, THRESHOLD_PATH)

    print("Saving plots...")
    plot_confusion_matrix(cm, CONFUSION_MATRIX_PLOT)
    plot_roc_curve(y_test, y_prob, ROC_CURVE_PLOT)
    plot_pr_curve(y_test, y_prob, PR_CURVE_PLOT)

    importance_df = generate_feature_importance(model, feature_columns, FEATURE_IMPORTANCE_PLOT)
    print("\nTop Features:")
    print(importance_df.head(15))

    print("Generating SHAP summary...")
    generate_shap_summary(model, X_test.iloc[:500], SHAP_SUMMARY_PLOT)

    print("\nTraining complete.")
    print("Saved in 'model' and 'report' folders.")


if __name__ == "__main__":
    main()