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

### Kaggle data
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


---

**Concepts demonstrated:** pivoting to a central dataset, financial metrics in numpy,
automated Excel reporting, Power BI data modelling (date table + DAX), dashboard design.
