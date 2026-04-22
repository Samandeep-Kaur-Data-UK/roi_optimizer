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

**New columns added to dataset:**
- `tv_adstock`
- `digital_adstock`
- `radio_adstock`

**Next:** Day 64 - Build the linear regression MMM using adstocked channels and
promo_flag as predictors. Extract coefficients to quantify ROI per pound spent.


## Day 64 - OLS Regression MMM Results

**Script:** `scripts/02_mmm_model.py`
**Outputs:** `outputs/mmm_model_summary.txt`

R-squared: 0.715
Adj R-squared: 0.703

| Channel | Coefficient | P-Value | Significant? |
|---------|-------------|---------|--------------|
| tv_adstock | 0.4281 | 0.0000 | YES |
| digital_adstock | 0.6875 | 0.0000 | YES |
| radio_adstock | 0.0724 | 0.6199 | NO |
| promo_flag | 8008.46 | 0.0000 | YES |

**Top channel by coefficient:** digital_adstock
**Finding:** Digital delivers the highest sales return per £1 of adstocked spend.
**Finding:** Radio is not statistically significant - budget should be reallocated.
**Finding:** Promotions add ~8,000 sales units independent of channel spend.

**Next:** Day 65 - Convert coefficients into ROI per £1 spent per channel.


## Day 65 - ROI Calculation per Channel

**Script:** `scripts/03_roi_calculator.py`
**Outputs:** `outputs/roi_by_channel.csv`, `outputs/roi_by_channel.png`

| Channel | Coefficient | Avg Weekly Spend | Avg Adstock | Return per £1 | ROI |
|---------|-------------|-----------------|-------------|---------------|-----|
| tv | 0.4281 | £11,996.47 | £29,592.65 | £1.06 | +5.59% |
| digital | 0.6875 | £8,937.62 | £12,714.81 | £0.98 | -2.20% |
| radio | 0.0724 | £4,666.85 | £7,750.90 | £0.12 | -87.97% |

**Top channel by ROI:** TV

**Key Findings:**
- TV is the only channel returning above break-even at £1.06 per £1 of effective spend
- Digital's coefficient is higher than TV but its ROI is lower because adstock carry-over is weaker at the current decay rate of 0.3
- Radio is statistically insignificant (p = 0.62 from Day 64) and destroys value at £0.12 return per £1 spent
- The gap between Day 64 (digital best coefficient) and Day 65 (TV best ROI) demonstrates why raw coefficients alone do not tell the full story - spend efficiency must be factored in

**Business Recommendation:**
Reallocate radio budget to TV immediately. Review digital spend levels as current allocation is operating just below break-even.

**Next:** Day 66 - Build budget optimiser to allocate £1,000 across channels by ROI weighting.


## Day 66 - Budget Optimiser

**Script:** `scripts/04_budget_optimizer.py`
**Outputs:** `outputs/budget_allocation.csv`, `outputs/budget_allocation.png`

### £1,000 Allocation Result

| Channel | Return per £1 | Recommended Spend | Weight | Expected Sales |
|---------|--------------|-------------------|--------|----------------|
| TV      | £1.06        | £1,000.00         | 100%   | £1,055.90      |
| Digital | £0.98        | £0.00             | 0%     | £0.00          |
| Radio   | £0.12        | £0.00             | 0%     | £0.00          |

Total expected sales return: £1,055.90

### £50,000 Allocation Result

| Channel | Return per £1 | Recommended Spend | Weight | Expected Sales |
|---------|--------------|-------------------|--------|----------------|
| TV      | £1.06        | £50,000.00        | 100%   | £52,795.00     |
| Digital | £0.98        | £0.00             | 0%     | £0.00          |
| Radio   | £0.12        | £0.00             | 0%     | £0.00          |

Total expected sales return: £52,795.00

**Logic:** Only channels above break-even (return per £1 > 1.0) receive budget.
Budget is weighted proportionally by ROI score.
Digital and Radio receive £0 allocation as both operate below break-even.

**Business finding:** At current ROI levels, every £1,000 invested entirely in TV
returns £1,055.90 in sales - a £55.90 net gain. Digital and Radio would destroy
value at current spend efficiency levels.

**Next:** Day 67 - Power BI MMM Results Dashboard.

## Day 67 - Power BI MMM Results Dashboard

**Tool:** Power BI Desktop (Windows 365)
**Outputs:** `powerbi/mmm_dashboard.pbix`, `outputs/day67_powerbi_demo_dashboard.png`

### Dashboard Structure

| Page | Visual | Description |
|------|--------|-------------|
| Page 1: KPIs | 4 Card visuals + Line chart + Bar chart + 2 Slicers | Top level performance summary |
| Page 2: Channel ROI | Clustered bar chart | Return per £1 by channel |
| Page 3: Budget Allocation | Pie chart + Table | Optimised spend recommendation |
| Page 4: Sales vs Spend | Dual-axis line chart | Sales trend overlaid with total spend |

### KPI Card Values (verified)

| Measure | Value |
|---------|-------|
| Total Sales | £1,941,048 |
| Total Spend | £2,662,497 |
| Promo Weeks | 23 |
| ROAS | 0.73 |

### DAX Measures Created

| Measure | Formula |
|---------|---------|
| Total Sales | SUM(marketing_data_powerbi[sales]) |
| TV Spend | SUM(marketing_data_powerbi[tv_spend]) |
| Digital Spend | SUM(marketing_data_powerbi[digital_spend]) |
| Radio Spend | SUM(marketing_data_powerbi[radio_spend]) |
| Total Spend | TV Spend + Digital Spend + Radio Spend |
| ROAS | DIVIDE(Total Sales, Total Spend) |
| Avg Weekly Sales | AVERAGE(marketing_data_powerbi[sales]) |
| Total Weeks | DISTINCTCOUNT(marketing_data_powerbi[week]) |
| Promo Weeks | SUM(marketing_data_powerbi[promo_flag]) |
| Promo Week % | DIVIDE(Promo Weeks, Total Weeks) |
| Sales In Promo Weeks | CALCULATE(Total Sales, promo_flag = 1) |
| Sales In Non Promo Weeks | CALCULATE(Total Sales, promo_flag = 0) |
| Rolling 4W Sales | CALCULATE(Total Sales, DATESINPERIOD(Date, MAX(Date), -28, DAY)) |

### Colour Schema

| Card | Background | Value | Label |
|------|-----------|-------|-------|
| Total Sales | #EEEDFE | #3C3489 | #534AB7 |
| Total Spend | #FAECE7 | #712B13 | #993C1D |
| Promo Weeks | #E1F5EE | #085041 | #0F6E56 |
| ROAS | #E6F1FB | #0C447C | #185FA5 |

**Status:** Page 1 KPI cards complete and verified. Line chart complete.
Bar chart and slicers in progress - to be completed Day 69 morning.

**Next:** Day 68 - Scenario analysis, then return to complete Pages 2, 3, 4.


## Day 68 - Sensitivity Analysis: What If Scenarios

**Script:** `scripts/05_scenario_analysis.py`
**Output:** `outputs/scenario_comparison.csv`

### Scenario Results

| Scenario | Predicted Sales | vs Baseline | Impact % |
|----------|----------------|-------------|----------|
| Baseline | £1,941,047 | £0 | 0.00% |
| A: Digital +20% / TV -20% | £1,859,385 | -£81,662 | -4.21% |
| B: Radio x2 / Digital -50% | £1,544,882 | -£396,165 | -20.41% |
| C: Remove TV / Digital +20% | £805,472 | -£1,135,575 | -58.50% |

### Key Findings

- No reallocation scenario improves on baseline sales
- Scenario C is catastrophic (-58.5%) confirming TV is the primary sales driver
- Scenario B confirms radio's weak coefficient (0.072) - doubling it cannot offset halving digital
- Scenario A is the least damaging reallocation but still loses £81K
- Business insight: the current channel mix is near-optimal - incremental total budget increase is a stronger lever than reallocation

**Status:** Complete. CSV exported and committed to GitHub.
Pending: Load scenario_comparison.csv into Power BI (to be done Day 69 morning).

**Next:** Day 69 - Complete Power BI dashboard Pages 2, 3, 4 and full pipeline test.