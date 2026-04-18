# ROI Optimizer - Project Notes

## Day 61: Setup

**Dataset:** 104 rows x 6 columns (2 years weekly data)
**Columns:** week, tv_spend, digital_spend, radio_spend, promo_flag, sales

**Finding:** No nulls across all 6 columns. Data types are correct (datetime, float, int).
Average weekly sales: £18,663. Digital spend shows highest mean relative to range,
suggesting it may be the most active channel. Promo flag fires 22% of weeks (23 of 104).
Sales range from £7,952 to £33,623 - good variance for modelling.

**Next:** Day 62 - Correlation matrix, scatter plots per channel, time series with promo highlights.


## Day 62 - EDA Findings

| Channel       | Correlation with Sales | Verdict         |
|---------------|------------------------|-----------------|
| tv_spend      | 0.530                  | Moderate driver |
| digital_spend | 0.489                  | Weak-moderate   |
| radio_spend   | 0.017                  | No relationship |

**Finding:** TV spend is the strongest channel predictor of sales (r = 0.530).
Digital spend shows a weaker but present relationship (r = 0.489). Radio spend
shows no meaningful correlation with sales (r = 0.017) and may not be a useful
model variable. Promo weeks show clear visible sales spikes in the time series,
suggesting promo_flag will be a strong predictor in the MMM model.

**Next:** Day 63 - Apply adstock transformations to each channel and compare
original vs adstocked spend before building the regression model.
