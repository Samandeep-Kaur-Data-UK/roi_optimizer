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

Current stage:
- Marketing dataset generated and quality-checked
- Exploratory analysis completed
- Correlation matrix exported
- Channel vs sales scatter plots created
- Weekly sales time-series with promo weeks highlighted created

Next stage:
- Implement adstock transformations for each channel
- Visualise original vs adstocked spend before modelling

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
