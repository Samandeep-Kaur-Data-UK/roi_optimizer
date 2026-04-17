import pandas as pd

df = pd.read_csv("data/marketing_data.csv", parse_dates=["week"])

print("=== Shape ===")
print(df.shape)

print("\n=== Info ===")
df.info()

print("\n=== Describe ===")
print(df.describe().round(2))

print("\n=== Head ===")
print(df.head())