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
- Scikit-learn
- Power BI

## Project Status

Day 63 complete in a 120-day analytics programme.

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

## Key Findings So Far

| Channel | Correlation with Sales | Adstock Decay | Avg Carry-Over Uplift |
|---------|------------------------|---------------|-----------------------|
| TV | r = 0.530 | 0.6 | +147% |
| Digital | r = 0.489 | 0.3 | +43% |
| Radio | r = 0.017 | 0.4 | +67% |

- TV shows the strongest raw relationship with sales and the longest ad memory
- Digital shows a weaker but meaningful relationship with fast decay
- Radio shows almost no correlation with sales (r = 0.017)
- Promo weeks align with visible sales spikes, `promo_flag` retained as model feature
- Without adstock, a regression using raw spend would underestimate TV's true contribution

## Next Stage

- Build linear regression MMM using adstocked channels and `promo_flag`
- Extract channel coefficients to quantify ROI per pound spent

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

## Structure

    roi_optimizer/
    ├── data/               # Source dataset, generator script, adstocked dataset
    ├── scripts/            # Inspection, EDA, and adstock scripts
    ├── outputs/            # Charts and model outputs
    ├── powerbi/            # Dashboard files
    ├── README.md
    └── project_notes.md