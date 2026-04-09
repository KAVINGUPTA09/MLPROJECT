import shap
import matplotlib.pyplot as plt
import pandas as pd


def generate_feature_importance(model, feature_columns, save_path):
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10, 6))
    top_n = importance_df.head(15)
    plt.barh(top_n["Feature"], top_n["Importance"])
    plt.gca().invert_yaxis()
    plt.title("Top 15 Feature Importances")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return importance_df


def generate_shap_summary(model, X_sample, save_path):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    plt.figure()
    shap.summary_plot(shap_values, X_sample, show=False)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()