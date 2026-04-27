# Day 67 Power BI Build Guide

## What caused the error

`marketing_data.csv` stores `week` as `dd/mm/yyyy`.
Power BI on your Windows setup is likely parsing dates as `mm/dd/yyyy`.
That means values like `16/01/2023` fail when you change the type directly to
Date.

## Fastest safe route

Use the Power BI-safe files in:

`data/powerbi`

Files:

- `marketing_data_powerbi.csv`
- `channel_spend_powerbi.csv`
- `mmm_data_adstocked_powerbi.csv`
- `roi_by_channel_powerbi.csv`
- `budget_allocation_powerbi.csv`

These already use ISO dates (`yyyy-mm-dd`) and safer column names.

## Recommended model for today

Load these 4 tables first:

1. `marketing_data_powerbi.csv`
2. `channel_spend_powerbi.csv`
3. `roi_by_channel_powerbi.csv`
4. `budget_allocation_powerbi.csv`

Optional for Page 3:

5. `mmm_data_adstocked_powerbi.csv`

## Why this model works

`marketing_data_powerbi` is a weekly fact table for sales and promo analysis.

`channel_spend_powerbi` is a channel-level fact table for spend visuals.

`roi_by_channel_powerbi` and `budget_allocation_powerbi` are channel summary
tables. They match `channel_spend_powerbi` by channel name.

Do not try to directly relate `roi_by_channel` to the original wide
`marketing_data` table by spend columns. The grains do not match.

## If you want to keep using the original marketing_data.csv

In Power Query:

1. Select `week`
2. Choose `Data Type` -> `Using Locale`
3. Data Type = `Date`
4. Locale = `English (United Kingdom)`

If needed, replace the step in Advanced Editor with:

```powerquery
= Table.TransformColumnTypes(#"Promoted Headers", {{"week", type date}}, "en-GB")
```

## Date table

Create this DAX table:

```DAX
Date =
ADDCOLUMNS(
    CALENDAR(
        MIN(marketing_data_powerbi[week]),
        MAX(marketing_data_powerbi[week])
    ),
    "Year", YEAR([Date]),
    "Month No", MONTH([Date]),
    "Month", FORMAT([Date], "MMM"),
    "Year Month", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & FORMAT([Date], "Q")
)
```

Mark `Date[Date]` as the date table.

## Relationships

Create these relationships:

1. `Date[Date]` -> `marketing_data_powerbi[week]` (one-to-many)
2. `Date[Date]` -> `channel_spend_powerbi[week]` (one-to-many)

Leave `roi_by_channel_powerbi` and `budget_allocation_powerbi` disconnected for
today unless you also create a small `Channel` dimension.

## Core measures

Create these measures in `marketing_data_powerbi`:

```DAX
Total Sales = SUM(marketing_data_powerbi[sales])

TV Spend = SUM(marketing_data_powerbi[tv_spend])

Digital Spend = SUM(marketing_data_powerbi[digital_spend])

Radio Spend = SUM(marketing_data_powerbi[radio_spend])

Total Spend =
    [TV Spend] + [Digital Spend] + [Radio Spend]

ROAS =
    DIVIDE([Total Sales], [Total Spend])

Avg Weekly Sales =
    AVERAGE(marketing_data_powerbi[sales])

Promo Weeks =
    SUM(marketing_data_powerbi[promo_flag])

Sales in Promo Weeks =
    CALCULATE(
        [Total Sales],
        marketing_data_powerbi[promo_flag] = 1
    )

Sales in Non-Promo Weeks =
    CALCULATE(
        [Total Sales],
        marketing_data_powerbi[promo_flag] = 0
    )

Rolling 4W Sales =
    CALCULATE(
        [Total Sales],
        DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -28, DAY)
    )
```

## Optional channel spend measure table

If you want cleaner by-channel visuals, use `channel_spend_powerbi` for them.
That table already has:

- `week`
- `channel`
- `spend`
- `promo_flag`

## Dashboard pages

### Page 1: Executive Summary

Use:

- Card: `Total Sales`
- Card: `Total Spend`
- Card: `ROAS`
- Card: `Promo Weeks`
- Line chart: `Date[Date]` vs `Total Sales`
- Clustered column chart: `Date[Year Month]` vs `TV Spend`, `Digital Spend`,
  `Radio Spend`
- Slicer: `Date[Year]`
- Slicer: `marketing_data_powerbi[promo_flag]`

### Page 2: Channel ROI

Use:

- Bar chart from `roi_by_channel_powerbi`
  - Axis: `channel`
  - Values: `return_per_gbp1`
- Bar chart from `roi_by_channel_powerbi`
  - Axis: `channel`
  - Values: `roi`
- Table from `budget_allocation_powerbi`
  - `channel`
  - `recommended_spend`
  - `weight_pct`
  - `expected_sales`
- Line chart from `channel_spend_powerbi`
  - Axis: `week`
  - Legend: `channel`
  - Values: `spend`

### Page 3: MMM / Adstock

Load `mmm_data_adstocked_powerbi.csv` and use:

- Line chart: `week` vs `tv_spend` and `tv_adstock`
- Bar chart: channel coefficients from `roi_by_channel_powerbi`
- Card: model R-squared = `0.715`
- Card: promo uplift = `8008.46`

## Narrative to show in the dashboard

- TV is the only channel above break-even at `1.0559` return per `£1`
- Digital is near break-even at `0.978`
- Radio is value-destructive at `0.1203`
- Promotions materially lift sales by about `8008`
- Recommendation: shift budget away from radio and toward TV

## Checked facts from the data

- 104 weekly rows
- Date range: `2023-01-02` to `2024-12-23`
- No nulls in the source data
- Total sales: `1,941,048.42`
- Total spend: `2,662,497.47`
- Promo weeks: `23`

## Best order to build today

1. Import `marketing_data_powerbi.csv`
2. Create the `Date` table
3. Build Page 1
4. Import `roi_by_channel_powerbi.csv` and `budget_allocation_powerbi.csv`
5. Build Page 2
6. Import `mmm_data_adstocked_powerbi.csv`
7. Build Page 3 only if time remains
