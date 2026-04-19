import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path

# --- Paths ---
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Load adstocked data (already computed in Day 63) ---
df = pd.read_csv(DATA_DIR / "mmm_data_adstocked.csv", parse_dates=["week"])

print(f"Loaded {len(df)} rows")
print(df.columns.tolist())

# --- Build OLS model ---
X = df[["tv_adstock", "digital_adstock", "radio_adstock", "promo_flag"]]
y = df["sales"]

X = sm.add_constant(X)  # adds intercept term

model = sm.OLS(y, X).fit()

# --- Print full summary to terminal ---
print("\n" + "="*60)
print(model.summary())
print("="*60)

# --- Save summary to file ---
summary_path = OUTPUT_DIR / "mmm_model_summary.txt"
with open(summary_path, "w") as f:
    f.write(str(model.summary()))
    f.write("\n\n--- Coefficients ---\n")
    f.write(str(model.params.to_string()))
    f.write("\n\n--- P-Values ---\n")
    f.write(str(model.pvalues.to_string()))
    f.write(f"\n\nR-squared:      {model.rsquared:.4f}\n")
    f.write(f"Adj R-squared:  {model.rsquared_adj:.4f}\n")

print(f"\nSummary saved to: {summary_path}")

# --- Identify top performing channel ---
channel_coeffs = model.params[["tv_adstock", "digital_adstock", "radio_adstock"]]
top_channel = channel_coeffs.idxmax()

print("\n--- Channel Coefficients ---")
for channel, coeff in channel_coeffs.items():
    pval = model.pvalues[channel]
    sig = "SIGNIFICANT" if pval < 0.05 else "not significant"
    print(f"  {channel:<20} coeff={coeff:.4f}   p={pval:.4f}  ({sig})")

print(f"\nTop channel: {top_channel}")
print(f"R-squared: {model.rsquared:.4f}")