# ROI Optimizer - Project Notes

## Day 61 - Setup & Data Inspection

**Script:** `scripts/01_inspect.py`
**Dataset:** 104 rows x 6 columns (2 years weekly data)
**Columns:** week, tv_spend, digital_spend, radio_spend, promo_flag, sales

| Metric | Value |
|--------|-------|
| Total weeks | 104 |
| Date range | Jan 2023 to Dec 2024 |
| Nulls | 0 across all columns |
| Avg weekly sales | £18,663 |
| Sales range | £7,952 to £33,623 |
| Promo weeks | 23 of 104 (22%) |

**Finding:** No nulls across all 6 columns. Data types are correct (datetime,
float, int). Average weekly sales: £18,663. Digital spend shows highest mean
relative to range, suggesting it may be the most active channel. Promo flag
fires 22% of weeks (23 of 104). Sales range from £7,952 to £33,623 - good
variance for modelling.

**Next:** Day 62 - Correlation matrix, scatter plots per channel, time series
with promo highlights.


## Day 62 - Exploratory Data Analysis

**Script:** `scripts/01_eda.py`
**Outputs:** `outputs/scatter_tv_spend_vs_sales.png`,
`outputs/scatter_digital_spend_vs_sales.png`,
`outputs/scatter_radio_spend_vs_sales.png`,
`outputs/timeseries_sales_promo.png`,
`outputs/correlation_matrix.csv`

| Channel | Correlation with Sales | Verdict |
|---------|------------------------|---------|
| tv_spend | 0.530 | Moderate driver |
| digital_spend | 0.489 | Weak-moderate |
| radio_spend | 0.017 | No relationship |

**Finding:** TV spend is the strongest channel predictor of sales (r = 0.530).
Digital spend shows a weaker but present relationship (r = 0.489). Radio spend
shows no meaningful correlation with sales (r = 0.017) and may not be a useful
model variable. Promo weeks show clear visible sales spikes in the time series,
suggesting promo_flag will be a strong predictor in the MMM model.

**Next:** Day 63 - Apply adstock transformations to each channel and compare
original vs adstocked spend before building the regression model.


## Day 63 - Adstock Transformation

**Script:** `scripts/03_adstock.py`
**Outputs:** `outputs/tv_adstock_plot.png`, `data/mmm_data_adstocked.csv`

### Adstock Formula
`adstock[t] = spend[t] + decay_rate * adstock[t-1]`

Each week carries forward a decayed fraction of the prior week's advertising
effect. Higher decay = longer memory. Lower decay = faster fade.

| Channel | Decay Rate | Avg Carry-Over Uplift | Rationale |
|---------|-----------|----------------------|-----------|
| TV | 0.6 | +147% | Long memory - brand ads linger for weeks |
| Digital | 0.3 | +43% | Short memory - performance ads fade fast |
| Radio | 0.4 | +67% | Medium memory - sits between TV and digital |

**Finding:** Adstock transformation makes the media series more commercially
realistic by carrying advertising impact into future weeks. TV adstock produces
an average carry-over uplift of 147% over raw spend - meaning a basic regression
using raw spend would severely underestimate TV's true contribution to sales.
The TV adstock line stays elevated after high-spend weeks, which is the expected
behaviour in an MMM workflow. Without adstock, any regression model would ignore
the carry-over zone entirely and produce misleading channel coefficients.

**New columns added to dataset:**
- `tv_adstock`
- `digital_adstock`
- `radio_adstock`

**Next:** Day 64 - Build the linear regression MMM using adstocked channels and
promo_flag as predictors. Extract coefficients to quantify ROI per pound spent.


## Day 64 - OLS Regression MMM Results

R-squared: 0.715
Adj R-squared: 0.703

| Channel          | Coefficient | P-Value | Significant? |
|------------------|-------------|---------|--------------|
| tv_adstock       | 0.4281      | 0.0000  | YES          |
| digital_adstock  | 0.6875      | 0.0000  | YES          |
| radio_adstock    | 0.0724      | 0.6199  | NO           |
| promo_flag       | 8008.46     | 0.0000  | YES          |

Top channel: digital_adstock
Finding: Digital delivers the highest sales return per £1 spent.
Finding: Radio is not statistically significant - budget should be reallocated.
Finding: Promotions add ~8,000 sales units independent of spend.