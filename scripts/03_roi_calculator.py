import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pathlib import Path

# --- Paths ---
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Load adstocked data ---
df = pd.read_csv(DATA_DIR / "mmm_data_adstocked.csv", parse_dates=["week"])

# --- Rebuild model (same as Day 64) ---
X = df[["tv_adstock", "digital_adstock", "radio_adstock", "promo_flag"]]
y = df["sales"]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

# --- Channel coefficients from model ---
coefficients = {
    "tv":      model.params["tv_adstock"],
    "digital": model.params["digital_adstock"],
    "radio":   model.params["radio_adstock"],
}

# --- Average spend per channel (from raw data) ---
avg_spend = {
    "tv":      df["tv_spend"].mean(),
    "digital": df["digital_spend"].mean(),
    "radio":   df["radio_spend"].mean(),
}

# --- Average adstock per channel ---
avg_adstock = {
    "tv":      df["tv_adstock"].mean(),
    "digital": df["digital_adstock"].mean(),
    "radio":   df["radio_adstock"].mean(),
}

# --- ROI calculation ---
# Incremental sales = coefficient * average adstock
# ROI = (incremental_sales / avg_spend) - 1
results = []
for channel in ["tv", "digital", "radio"]:
    incremental_sales = coefficients[channel] * avg_adstock[channel]
    roi = (incremental_sales / avg_spend[channel]) - 1
    results.append({
        "channel":            channel,
        "coefficient":        round(coefficients[channel], 4),
        "avg_weekly_spend":   round(avg_spend[channel], 2),
        "avg_adstock":        round(avg_adstock[channel], 2),
        "incremental_sales":  round(incremental_sales, 2),
        "roi":                round(roi, 4),
        "return_per_£1":      round(roi + 1, 4),
    })

roi_df = pd.DataFrame(results).sort_values("roi", ascending=False)

# --- Print results ---
print("\n--- ROI per Channel ---")
print(roi_df.to_string(index=False))

# --- Save to CSV ---
roi_path = OUTPUT_DIR / "roi_by_channel.csv"
roi_df.to_csv(roi_path, index=False)
print(f"\nROI table saved to: {roi_path}")

# --- Bar chart ---
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#4CAF50" if r > 0 else "#F44336" for r in roi_df["roi"]]
ax.bar(roi_df["channel"], roi_df["return_per_£1"], color=colors, edgecolor="white")
ax.axhline(y=1, color="black", linestyle="--", linewidth=0.8, label="Break-even (£1 in = £1 out)")
ax.set_title("ROI per Channel: Sales Return per £1 Spent", fontsize=13, fontweight="bold")
ax.set_xlabel("Channel")
ax.set_ylabel("£ Sales Return per £1 Spent")
ax.legend()
plt.tight_layout()
chart_path = OUTPUT_DIR / "roi_by_channel.png"
plt.savefig(chart_path, dpi=150)
plt.close()
print(f"Chart saved to: {chart_path}")

# --- Summary statement ---
top = roi_df.iloc[0]
print(f"\nTop channel: {top['channel'].upper()}")
print(f"For every £1 spent on {top['channel']}, the model returns £{top['return_per_£1']:.2f} in sales.")