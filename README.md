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

Day 65 complete in a 120-day analytics programme.

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
- Key insight: digital has a higher coefficient than TV but lower ROI because its adstock carry-over is weaker at decay rate 0.3 vs TV's 0.6 - raw coefficients alone do not tell the full story
- Saved ROI table to `outputs/roi_by_channel.csv` and bar chart to `outputs/roi_by_channel.png`

## Key Findings

### Correlation vs Sales (Pre-Model)

| Channel | Correlation with Sales | Adstock Decay | Avg Carry-Over Uplift |
|---------|------------------------|---------------|-----------------------|
| TV | r = 0.530 | 0.6 | +147% |
| Digital | r = 0.489 | 0.3 | +43% |
| Radio | r = 0.017 | 0.4 | +67% |

### OLS Regression Results (Day 64)

| Channel | Coefficient | P-Value | Significant? |
|---------|-------------|---------|--------------|
| digital_adstock | 0.6875 | 0.0000 | YES |
| tv_adstock | 0.4281 | 0.0000 | YES |
| radio_adstock | 0.0724 | 0.6199 | NO |
| promo_flag | 8008.46 | 0.0000 | YES |

**Model R-squared: 0.715**

### ROI per Channel (Day 65)

| Channel | Coefficient | Avg Weekly Spend | Avg Adstock | Return per £1 | ROI |
|---------|-------------|-----------------|-------------|---------------|-----|
| TV | 0.4281 | £11,996.47 | £29,592.65 | £1.06 | +5.59% |
| Digital | 0.6875 | £8,937.62 | £12,714.81 | £0.98 | -2.20% |
| Radio | 0.0724 | £4,666.85 | £7,750.90 | £0.12 | -87.97% |

**Business Recommendation:** Reallocate radio budget to TV immediately. Review digital spend levels as current allocation is operating just below break-even.

## Next Stage

- Build £1,000 budget allocation optimiser weighted by channel ROI
- Visualise ROI comparison and budget allocation in Power BI

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

## Structure

    roi_optimizer/
    ├── data/               # Source dataset, generator script, adstocked dataset
    ├── scripts/            # Inspection, EDA, adstock, regression, and ROI scripts
    ├── outputs/            # Charts and model outputs
    ├── powerbi/            # Dashboard files
    ├── README.md
    └── project_notes.md