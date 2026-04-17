# ROI Optimizer - Project Notes

## Day 61: Setup

**Dataset:** 104 rows x 6 columns (2 years weekly data)
**Columns:** week, tv_spend, digital_spend, radio_spend, promo_flag, sales

**Finding:** No nulls across all 6 columns. Data types are correct (datetime, float, int).
Average weekly sales: £18,663. Digital spend shows highest mean relative to range,
suggesting it may be the most active channel. Promo flag fires 22% of weeks (23 of 104).
Sales range from £7,952 to £33,623 - good variance for modelling.

**Next:** Day 62 - Correlation matrix, scatter plots per channel, time series with promo highlights.