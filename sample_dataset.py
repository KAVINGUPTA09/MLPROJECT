import pandas as pd

# original big dataset ka path
df = pd.read_csv("B:/creditcard.csv")

# 10,000 rows ka sample
df_small = df.sample(10000, random_state=42)

# new small dataset save
df_small.to_csv("data/creditcard.csv", index=False)

print("✅ Small dataset created successfully!")