## The Business Problem
A UK brand was spending across TV, Digital, and Radio with no data 
on which channel was actually driving revenue.

## What I Built
A Marketing Mix Model in Python using OLS regression and adstock 
transformation to isolate the true contribution of each channel.

## What the Model Found
- TV: only channel above break-even at £1.056 return per £1 spent
- Digital: near break-even at £0.978
- Radio: value destructive at £0.120

## The Business Recommendation
Concentrate the next £1,000 into TV. Every reallocation away from 
TV destroys revenue — removing it entirely cuts predicted sales by 58.5%.

## The Numbers That Matter (not the model metrics)
Incremental revenue from optimised allocation: £1,055.90 per £1,000
Scenario C worst case loss: -£1,135,575 (-58.50%)

## Interview Q&A

**Q: How did you validate the model?**
Train/test split on time-series data. Checked R-squared, reviewed residual plots for patterns, and confirmed coefficients matched business logic (TV being the most mature channel, expected higher baseline ROI).

**Q: What are the limitations of OLS regression?**
Assumes linear relationships between spend and sales — real-world returns diminish at high spend levels. Also assumes no multicollinearity between channels, which is rarely true. OLS cannot capture competitive activity or external shocks (seasonality, economic events).

**Q: How would you improve this with more data?**
More granular time series (weekly to daily) to improve adstock decay estimates. Add competitor spend data. Move from OLS to a Bayesian MMM (e.g. using PyMC) to get uncertainty ranges around ROI estimates rather than point estimates — more credible to a senior stakeholder.