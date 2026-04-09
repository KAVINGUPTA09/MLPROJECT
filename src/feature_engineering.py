import numpy as np
def add_engineered_features(df):
    df = df.copy()

    if "Amount" in df.columns:
        df["Amount_log"] = np.log1p(df["Amount"].clip(lower=0))
        df["High_Amount_Flag"] = (df["Amount"] > df["Amount"].quantile(0.95)).astype(int)

    if "Time" in df.columns:
        df["Hour"] = (df["Time"] // 3600) % 24
        df["Night_Transaction"] = df["Hour"].isin([0, 1, 2, 3, 4, 23]).astype(int)

    return df