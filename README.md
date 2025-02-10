# Conditional Drawdown

## Overview

`conditional-drawdown` is a Python library designed for reliable drawdown risk analysis, using the Conditional Expected Drawdown (CED) metric. Unlike traditional risk metrics like volatility or Value-at-Risk, CED accounts for the path dependency of drawdowns and provides a robust measure of extreme risk. This tool is ideal for portfolio managers, risk analysts, and quantitative researchers.

Key features include:

- **Maximum Drawdown (MDD):** Calculates the largest cumulative loss from peak to trough over a given time period.
- **Rolling Maximum Drawdown (RMD):** Computes drawdowns over sliding windows to track evolving risks.
- **Conditional Expected Drawdown (CED):** Estimates the expected maximum drawdown given that a threshold is breached, enabling deeper insights into tail risk.
- **Portfolio Risk Attribution:(WIP)** Analyze and attribute risk contributions across assets or factors using CED.

## Installation

You can install the library via pip:

```bash
pip install conditional-drawdown
```
# Usage

```python
from conditional_drawdown import CED, max_drawdown, rolling_max_drawdown
import yfinance as yf

# Download historical data
tickers = ["ES=F", "GLD"]
data = yf.download(tickers, end="2023-12-31")["Adj Close"]

# Calculate returns
returns = data.pct_change().dropna()

# Compute Conditional Expected Drawdown (CED)
es_ced = CED(returns['ES=F'].values)
gld_ced = CED(returns['GLD'].values)

print(f"S&P Futures CED: {es_ced}")
print(f"Gold ETF CED: {gld_ced}")

# Portfolio example
portfolio_returns = (returns * 0.5).sum(axis=1)
portfolio_ced = CED(portfolio_returns.values)
print(f"Portfolio CED: {portfolio_ced}")
```
# Features

- Maximum Drawdown (MDD):
Calculates the largest cumulative loss from peak to trough in a return series.
Example:
```py
    max_dd = max_drawdown(returns['ES=F'].values)
    print(f"Max Drawdown: {max_dd}")
```

- Rolling Maximum Drawdown (RMD):

Computes MDD over rolling windows, enabling time-sensitive risk tracking.
Example:
```py
    rmd = rolling_max_drawdown(returns['GLD'].values, window=21)
    print(f"Rolling Max Drawdown: {rmd}")
```
- Conditional Expected Drawdown (CED):

Focuses on the tail-end of drawdown distributions, providing a measure of extreme risk exposure.
Example:
```py
        ced = CED(returns['GLD'].values, t=21, alpha=0.9)
        print(f"Conditional Expected Drawdown: {ced}")
```
### Why CED?

- Path Dependency: CED captures consecutive losses, unlike volatility or Value-at-Risk.
- Convex and Linear: Useful for portfolio optimization and risk attribution.
- Tail Risk Sensitivity: Ideal for stress-testing portfolios under extreme market conditions.

## Contributing

Contributions are welcome! Please follow these steps:

- Fork the repository.
- Create a feature branch: git checkout -b feat/feature-name
- Commit your changes: git commit -m 'Add new feature'
- Push to your branch: git push origin feature-name
- Open a pull request.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Inspired by the work of Lisa R. Goldberg and Ola Mahmoud, Drawdown: From Practice to Theory and Back Again.
arXiv:1404.7493
