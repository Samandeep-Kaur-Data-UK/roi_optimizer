import pandas as pd

# Model coefficients from OLS regression
CONST = -5076.853221
TV_COEF = 0.428053
DIGITAL_COEF = 0.687478
RADIO_COEF = 0.072417
PROMO_COEF = 8008.456978

# Load adstocked data
df = pd.read_csv('data/mmm_data_adstocked.csv')

# Predict sales function
def predict_sales(tv, digital, radio, promo):
    return (CONST + (TV_COEF * tv) + (DIGITAL_COEF * digital) + (RADIO_COEF * radio) + (PROMO_COEF * promo)).sum()

# Baseline
baseline = predict_sales(df['tv_adstock'], df['digital_adstock'], df['radio_adstock'], df['promo_flag'])

# Scenario A: Digital +20%, TV -20%
scenario_a = predict_sales(df['tv_adstock'] * 0.80, df['digital_adstock'] * 1.20, df['radio_adstock'], df['promo_flag'])

# Scenario B: Radio x2, Digital -50%
scenario_b = predict_sales(df['tv_adstock'], df['digital_adstock'] * 0.50, df['radio_adstock'] * 2.0, df['promo_flag'])

# Scenario C: TV removed, Digital +20%
scenario_c = predict_sales(df['tv_adstock'] * 0, df['digital_adstock'] * 1.20, df['radio_adstock'], df['promo_flag'])

# Build results table
results = pd.DataFrame({
    'Scenario': [
        'Baseline',
        'A: Digital +20% / TV -20%',
        'B: Radio x2 / Digital -50%',
        'C: Remove TV / Digital +20%'
    ],
    'Predicted Sales (£)': [
        round(baseline, 2),
        round(scenario_a, 2),
        round(scenario_b, 2),
        round(scenario_c, 2)
    ]
})

results['vs Baseline (£)'] = (results['Predicted Sales (£)'] - baseline).round(2)
results['Impact %'] = ((results['vs Baseline (£)'] / baseline) * 100).round(2)

print(results.to_string(index=False))

results.to_csv('outputs/scenario_comparison.csv', index=False)
print("\nSaved to outputs/scenario_comparison.csv")