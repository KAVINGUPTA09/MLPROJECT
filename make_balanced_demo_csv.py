import pandas as pd

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Separate classes
fraud_df = df[df["Class"] == 1]
normal_df = df[df["Class"] == 0]

print("Fraud rows available:", len(fraud_df))
print("Legitimate rows available:", len(normal_df))

# Take as many fraud rows as available, max 50
n_fraud = min(50, len(fraud_df))

# Take same number of legitimate rows for balance
n_normal = n_fraud

# Sample
fraud_sample = fraud_df.sample(n=n_fraud, random_state=42, replace=False)
normal_sample = normal_df.sample(n=n_normal, random_state=42, replace=False)

# Combine and shuffle
demo_df = pd.concat([fraud_sample, normal_sample], axis=0)
demo_df = demo_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save both versions
demo_df.to_csv("balanced_demo_with_class.csv", index=False)
demo_df.drop(columns=["Class"]).to_csv("balanced_demo_upload.csv", index=False)

print("\nFiles created successfully:")
print("1. balanced_demo_with_class.csv")
print("2. balanced_demo_upload.csv")
print(f"Total rows saved: {len(demo_df)}")
print(f"Fraud rows used: {n_fraud}")
print(f"Legitimate rows used: {n_normal}")