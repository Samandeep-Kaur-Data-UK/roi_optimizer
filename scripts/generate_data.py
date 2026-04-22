import pandas as pd
import numpy as np

np.random.seed(42)
weeks = pd.date_range(start="2023-01-02", periods=104, freq="W-MON")

tv_spend = np.random.uniform(5000, 20000, 104)
digital_spend = np.random.uniform(3000, 15000, 104)
radio_spend = np.random.uniform(1000, 8000, 104)
promo_flag = np.random.choice([0, 1], size=104, p=[0.8, 0.2])

# Sales driven by spend + promo + noise
sales = (
    0.6 * tv_spend
    + 0.9 * digital_spend
    + 0.3 * radio_spend
    + 8000 * promo_flag
    + np.random.normal(0, 3000, 104)
)

df = pd.DataFrame({
    "week": weeks,
    "tv_spend": tv_spend.round(2),
    "digital_spend": digital_spend.round(2),
    "radio_spend": radio_spend.round(2),
    "promo_flag": promo_flag,
    "sales": sales.round(2)
})

df.to_csv("data/marketing_data.csv", index=False)
print("Generated marketing_data.csv")
print(df.head())