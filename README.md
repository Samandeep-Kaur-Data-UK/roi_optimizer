# ROI Optimizer: Marketing Mix Model (MMM)

## Overview
ROI Optimizer is a Marketing Mix Modelling project built in Python to estimate
how TV, digital, and radio spend contribute to weekly sales. The commercial
question behind the project is simple: where should the next marketing budget be
allocated for the strongest return?

## Tech Stack
- Python
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Power BI

## Project Status
Day 62 complete in a 120-day analytics programme.

Completed so far:
- Day 61: project setup, synthetic marketing dataset creation, and data quality checks
- Day 62: exploratory analysis, correlation review, scatter plots, and promo time-series visualisation

Next stage:
- Implement adstock transformations for each channel
- Visualise original vs adstocked spend before modelling

## Progress Log
### Day 61 - Project Setup
- Created the MMM project structure and generated a 104-row weekly marketing dataset
- Confirmed the dataset contains no missing values and the data types are correct
- Established the modelling base with `week`, channel spend, `promo_flag`, and `sales`

### Day 62 - Exploratory Analysis
- Calculated the correlation matrix for TV, digital, radio, and sales
- Built three scatter plots to compare channel spend vs sales
- Built a weekly sales time-series chart with promo weeks highlighted
- Documented which channels appear most commercially relevant before modelling

## Day 62 Key Findings
- `TV` shows the strongest relationship with sales (`r = 0.530`)
- `Digital` shows a weaker but still meaningful relationship (`r = 0.489`)
- `Radio` shows almost no relationship with sales (`r = 0.017`)
- Promo weeks align with visible sales spikes, suggesting `promo_flag` should
  be retained as a model feature

## Outputs
- `outputs/correlation_matrix.csv`
- `outputs/scatter_tv_spend_vs_sales.png`
- `outputs/scatter_digital_spend_vs_sales.png`
- `outputs/scatter_radio_spend_vs_sales.png`
- `outputs/timeseries_sales_promo.png`

## Structure
```text
roi_optimizer/
├── data/            # Source dataset and generator script
├── scripts/         # Inspection and EDA scripts
├── outputs/         # Charts and correlation outputs
├── powerbi/         # Dashboard files
├── README.md
└── project_notes.md
```
