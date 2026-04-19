## Day 65 - ROI Calculation per Channel

**Script:** `scripts/03_roi_calculator.py`
**Outputs:** `outputs/roi_by_channel.csv`, `outputs/roi_by_channel.png`

| Channel | Coefficient | Avg Weekly Spend | Avg Adstock | Return per £1 | ROI |
|---------|-------------|-----------------|-------------|---------------|-----|
| tv      | 0.4281      | £11,996.47      | £29,592.65  | £1.06         | +5.59% |
| digital | 0.6875      | £8,937.62       | £12,714.81  | £0.98         | -2.20% |
| radio   | 0.0724      | £4,666.85       | £7,750.90   | £0.12         | -87.97% |

**Top channel by ROI:** TV

**Key Findings:**
- TV is the only channel returning above break-even at £1.06 per £1 of effective spend
- Digital's coefficient is higher than TV but its ROI is lower because adstock carry-over is weaker at the current decay rate of 0.3
- Radio is statistically insignificant (p = 0.62 from Day 64) and destroys value at £0.12 return per £1 spent
- The gap between Day 64 (digital best coefficient) and Day 65 (TV best ROI) demonstrates why raw coefficients alone do not tell the full story - spend efficiency must be factored in

**Business Recommendation:**
Reallocate radio budget to TV immediately. Review digital spend levels as current allocation is operating just below break-even.

**Next:** Day 66 - Build budget optimiser to allocate £1,000 across channels by ROI weighting.