# Immersive Analytics Portfolio

**A central financial dataset, an interactive Power BI dashboard for portfolio analysis,
and automated reporting templates in Excel and Python.**

This project takes daily stock-price data, builds a single clean **central dataset**, and
turns it into portfolio analytics: returns, risk, allocation and drawdown — delivered both
as an automated Excel report and an interactive dashboard.

---

## What it does

| Stage | Tool | Output |
|-------|------|--------|
| 1. Central dataset | Python (pandas) | Tidy price + weight fact table from raw financial data |
| 2. Portfolio analytics | Python (numpy) | Returns, volatility, Sharpe, correlation, drawdown |
| 3. Automated reporting | Excel (openpyxl) | Multi-sheet `portfolio_report.xlsx` template |
| 4. Interactive dashboard | Power BI **and** Plotly | Portfolio analysis dashboards |

## Metrics produced
- **Annualised return & volatility** per asset and for the whole portfolio
- **Sharpe ratio** (risk-adjusted return)
- **Correlation matrix** across holdings
- **Growth of 1€** invested (cumulative return)
- **Maximum drawdown** (worst peak-to-trough loss)
- **Allocation** by weight

---

## How to run

You can run on **real Kaggle data** (recommended) or on built-in synthetic data.

### Option A — real Kaggle data (recommended)
Dataset: [S&P 500 stock data](https://www.kaggle.com/datasets/camnugent/sandp500) (by *camnugent*).
1. Download `all_stocks_5yr.csv` from that page (free Kaggle account) into the `data/` folder.
2. Run:
```bash
pip install -r requirements.txt
python data/load_kaggle.py     # filter to 6 tickers + a date window -> data/prices.csv
python build_portfolio.py      # central dataset + Excel report + Plotly dashboard
```
`load_kaggle.py` keeps a small slice (6 tickers, ~3 years) so the dataset stays manageable —
edit the `TICKERS` / `START` / `END` values at the top of that file to change it.

### Option B — synthetic data (no download needed)
```bash
pip install -r requirements.txt
python data/generate_data.py   # generate data/prices.csv (Geometric Brownian Motion)
python build_portfolio.py
```

Either way, open `dashboard/portfolio_dashboard.html` in a browser and build the Power BI
version with [`powerbi/POWERBI_GUIDE.md`](powerbi/POWERBI_GUIDE.md). The analytics code is
identical for real and synthetic data — only the source CSV differs.

---

## How to talk about this project (interview)

> "I built a portfolio-analytics project: I consolidated daily financial data into one
> central dataset, then computed portfolio metrics — returns, volatility, the Sharpe ratio,
> correlations and drawdown. I automated an Excel reporting template so the numbers refresh
> from the data, and I built an interactive dashboard in Power BI with a date table and DAX
> measures, plus a Python/Plotly version. It's about turning raw data into a clear,
> repeatable report a decision-maker can use."

**Concepts demonstrated:** pivoting to a central dataset, financial metrics in numpy,
automated Excel reporting, Power BI data modelling (date table + DAX), dashboard design.
