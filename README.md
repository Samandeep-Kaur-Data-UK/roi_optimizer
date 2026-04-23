# ROI Optimizer: Marketing Mix Model (MMM)

## Overview

ROI Optimizer is a Marketing Mix Modelling project built in Python to estimate
how TV, digital, and radio spend contribute to weekly sales. The commercial
question behind the project is simple: where should the next marketing budget
be allocated for the strongest return?

## Tech Stack

- Python 3.14
- Pandas
- Matplotlib
- Statsmodels
- Scikit-learn
- Power BI

## Project Status

Day 70 complete in a 120-day analytics programme.

## Progress Log

### Day 61 - Project Setup

- Created the MMM project structure and generated a 104-row weekly marketing dataset
- Confirmed the dataset contains no missing values and data types are correct
- Established the modelling base with `week`, channel spend, `promo_flag`, and `sales`

### Day 62 - Exploratory Data Analysis

- Calculated the correlation matrix for TV, digital, radio, and sales
- Built three scatter plots to compare channel spend vs sales
- Built a weekly sales time-series chart with promo weeks highlighted
- Documented which channels appear most commercially relevant before modelling

### Day 63 - Adstock Transformation

- Implemented geometric adstock: `adstock[t] = spend[t] + decay_rate * adstock[t-1]`
- Applied decay rates: TV = 0.6, Digital = 0.3, Radio = 0.4
- Visualised original vs adstocked TV spend across 104 weeks
- Exported adstocked dataset ready for regression modelling

### Day 64 - OLS Regression Model

- Built an OLS (Ordinary Least Squares) regression using statsmodels
- Inputs: tv_adstock, digital_adstock, radio_adstock, promo_flag
- Output: weekly sales
- Model achieved R-squared of 0.715 - explaining 71.5% of all sales variation
- Extracted channel coefficients to quantify sales return per £1 of adstocked spend
- Identified radio as statistically insignificant (p = 0.62)
- Saved full model summary to `outputs/mmm_model_summary.txt`

### Day 65 - ROI Calculation per Channel

- Converted OLS coefficients into ROI per £1 of effective spend per channel
- TV is the top performing channel at £1.06 return per £1 spent (ROI +5.59%)
- Digital operates just below break-even at £0.98 return per £1 spent (ROI -2.20%)
- Radio destroys value at £0.12 return per £1 spent (ROI -87.97%)
- Key insight: digital has a higher coefficient than TV but lower ROI because its
  adstock carry-over is weaker at decay rate 0.3 vs TV's 0.6 - raw coefficients
  alone do not tell the full story
- Saved ROI table to `outputs/roi_by_channel.csv` and bar chart to `outputs/roi_by_channel.png`

### Day 66 - Budget Optimiser

- Built a CLI budget optimisation tool using `argparse` - accepts any budget as input
- Logic: only channels above break-even (return per £1 > 1.0) receive allocation
- Budget is weighted proportionally by ROI score across profitable channels
- At current ROI levels, 100% of budget allocated to TV as the only profitable channel
- £1,000 input returns £1,055.90 in expected sales (net gain of £55.90)
- Digital and Radio receive £0 allocation until spend efficiency improves
- Saved allocation table to `outputs/budget_allocation.csv` and chart to `outputs/budget_allocation.png`

### Day 67 - Power BI MMM Results Dashboard (In Progress)

- Dashboard build started - KPI page complete with Total Sales, Total Spend, ROAS, Promo Weeks
- Weekly Sales Trend line chart and Spend by Channel bar chart live on Page 1
- Pages 2, 3, and 4 in progress - continuing Day 69

### Day 68 - Scenario Analysis

- Built scenario analysis script to model 3 budget reallocation strategies
- Used OLS coefficients to predict sales impact of each scenario
- Scenario A (Digital +20% / TV -20%): sales drop -4.21% (-£81,662)
- Scenario B (Radio x2 / Digital -50%): sales drop -20.41% (-£396,165)
- Scenario C (Remove TV / Digital +20%): sales drop -58.50% (-£1,135,575)
- Key insight: no reallocation improves baseline - current mix is near-optimal
- Saved results to `outputs/scenario_comparison.csv`

### Day 69 - Power BI Dashboard Continued (In Progress)

- Channel ROI Bar Chart page in progress using real model outputs from roi_by_channel_powerbi.csv
- Budget Allocation and Scenario pages to follow
- HTML interactive dashboard built as parallel portfolio deliverable

### Day 70 - Presentation Preparation

- Written verbal walkthrough of the full MMM project in `presentation_notes.md`
- Framed as a business story: problem, method, findings, and recommendation
- Prepared interview answers covering model validation, OLS limitations, and improvement paths
- Key framing: lead with incremental revenue outcomes, not model metrics

## Key Findings

### Correlation vs Sales (Pre-Model)

| Channel | Correlation with Sales | Adstock Decay | Avg Carry-Over Uplift |
|---------|------------------------|---------------|-----------------------|
| TV      | r = 0.530              | 0.6           | +147%                 |
| Digital | r = 0.489              | 0.3           | +43%                  |
| Radio   | r = 0.017              | 0.4           | +67%                  |

### OLS Regression Results (Day 64)

| Channel          | Coefficient | P-Value | Significant? |
|------------------|-------------|---------|--------------|
| digital_adstock  | 0.6875      | 0.0000  | YES          |
| tv_adstock       | 0.4281      | 0.0000  | YES          |
| radio_adstock    | 0.0724      | 0.6199  | NO           |
| promo_flag       | 8008.46     | 0.0000  | YES          |

**Model R-squared: 0.715**

### ROI per Channel (Day 65)

| Channel | Coefficient | Avg Weekly Spend | Avg Adstock  | Return per £1 | ROI      |
|---------|-------------|-----------------|--------------|---------------|----------|
| TV      | 0.4281      | £11,996.47      | £29,592.65   | £1.06         | +5.59%   |
| Digital | 0.6875      | £8,937.62       | £12,714.81   | £0.98         | -2.20%   |
| Radio   | 0.0724      | £4,666.85       | £7,750.90    | £0.12         | -87.97%  |

### Budget Allocation (Day 66)

| Channel | Return per £1 | £1,000 Allocation | Expected Sales |
|---------|--------------|-------------------|----------------|
| TV      | £1.06        | £1,000.00         | £1,055.90      |
| Digital | £0.98        | £0.00             | £0.00          |
| Radio   | £0.12        | £0.00             | £0.00          |

**Business Recommendation:** At current ROI levels, allocate 100% of marketing
budget to TV. Revisit digital spend efficiency before increasing its allocation.
Eliminate radio spend entirely.

### Scenario Analysis (Day 68)

| Scenario                    | Predicted Sales | vs Baseline  | Impact %  |
|-----------------------------|----------------|--------------|-----------|
| Baseline                    | £1,941,047     | £0           | 0.00%     |
| A: Digital +20% / TV -20%   | £1,859,385     | -£81,662     | -4.21%    |
| B: Radio x2 / Digital -50%  | £1,544,882     | -£396,165    | -20.41%   |
| C: Remove TV / Digital +20% | £805,472       | -£1,135,575  | -58.50%   |

**Business Insight:** No reallocation scenario improves on baseline sales.
The current channel mix is near-optimal. Increasing total budget is a stronger
lever than reallocating between channels.

## Outputs

| File | Description |
|------|-------------|
| `outputs/correlation_matrix.csv` | Pearson r values across all channels |
| `outputs/scatter_tv_spend_vs_sales.png` | TV spend vs sales scatter |
| `outputs/scatter_digital_spend_vs_sales.png` | Digital spend vs sales scatter |
| `outputs/scatter_radio_spend_vs_sales.png` | Radio spend vs sales scatter |
| `outputs/timeseries_sales_promo.png` | Weekly sales with promo highlights |
| `outputs/tv_adstock_plot.png` | TV original vs adstocked spend |
| `data/mmm_data_adstocked.csv` | Dataset with adstock columns added |
| `outputs/mmm_model_summary.txt` | Full OLS regression results |
| `outputs/roi_by_channel.csv` | ROI per channel table |
| `outputs/roi_by_channel.png` | ROI bar chart by channel |
| `outputs/budget_allocation.csv` | Recommended budget allocation table |
| `outputs/budget_allocation.png` | Budget allocation and expected sales chart |
| `outputs/scenario_comparison.csv` | 3 scenario budget reallocation results vs baseline |
| `presentation_notes.md` | Business story walkthrough and interview Q&A |

## Structure

    roi_optimizer/
    ├── data/               # Source dataset, generator script, adstocked dataset
    ├── scripts/            # Inspection, EDA, adstock, regression, ROI, optimiser, scenario scripts
    ├── outputs/            # Charts and model outputs
    ├── powerbi/            # Dashboard files
    ├── README.md
    └── presentation_notes.md