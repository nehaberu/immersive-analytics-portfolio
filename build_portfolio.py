"""
Immersive Analytics Portfolio : build the central dataset + automated reports.

Steps:
  1. Load data/prices.csv (the "central data base" of financial data).
  2. Compute portfolio analytics: daily & cumulative returns, volatility, Sharpe,
     correlation, and a weighted portfolio value.
  3. Produce automated outputs:
        - data/portfolio_facts.csv   -> clean star-schema-style fact table for Power BI
        - reports/portfolio_report.xlsx  -> automated multi-sheet Excel report (template)
        - dashboard/portfolio_dashboard.html -> interactive Plotly dashboard (Python)

Run:  python build_portfolio.py   (after data/generate_data.py)
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent

# Portfolio weights (must sum to 1.0) — equal-ish with a defensive tilt.
WEIGHTS = {"AAPL": 0.22, "MSFT": 0.22, "AMZN": 0.18, "JPM": 0.15, "KO": 0.13, "XOM": 0.10}
TRADING_DAYS = 252
RISK_FREE = 0.02   # annual


def main():
    prices = pd.read_csv(HERE / "data" / "prices.csv", parse_dates=["Date"])

    # ---- central dataset: wide matrix of closing prices (Date x Ticker) ----
    close = prices.pivot(index="Date", columns="Ticker", values="Close").sort_index()

    # Keep only tickers we have a target weight for, then renormalise the weights
    # so they still sum to 1.0. This makes the project robust whether the data is
    # synthetic (generate_data.py) or real (load_kaggle.py).
    present = [t for t in WEIGHTS if t in close.columns]
    close = close[present]
    weights = pd.Series({t: WEIGHTS[t] for t in present})
    weights = weights / weights.sum()

    daily_ret = close.pct_change().dropna()

    # ---- per-asset metrics ----
    ann_return = (1 + daily_ret.mean()) ** TRADING_DAYS - 1
    ann_vol = daily_ret.std() * np.sqrt(TRADING_DAYS)
    sharpe = (ann_return - RISK_FREE) / ann_vol
    per_asset = pd.DataFrame({
        "Ticker": close.columns,
        "Weight": [weights[t] for t in close.columns],
        "AnnReturn": ann_return.round(4).values,
        "AnnVolatility": ann_vol.round(4).values,
        "Sharpe": sharpe.round(2).values,
    })

    # ---- portfolio-level series ----
    w = weights[close.columns]
    port_daily = daily_ret.dot(w)
    port_cum = (1 + port_daily).cumprod()
    port_ann_return = (1 + port_daily.mean()) ** TRADING_DAYS - 1
    port_ann_vol = port_daily.std() * np.sqrt(TRADING_DAYS)
    port_sharpe = (port_ann_return - RISK_FREE) / port_ann_vol
    drawdown = port_cum / port_cum.cummax() - 1
    max_dd = drawdown.min()

    print("Portfolio summary")
    print(f"  Annualised return : {port_ann_return:6.2%}")
    print(f"  Annualised vol    : {port_ann_vol:6.2%}")
    print(f"  Sharpe ratio      : {port_sharpe:6.2f}")
    print(f"  Max drawdown      : {max_dd:6.2%}")

    # ---- fact table for Power BI (long, tidy) ----
    facts = prices.merge(per_asset[["Ticker", "Weight"]], on="Ticker", how="left")
    facts.to_csv(HERE / "data" / "portfolio_facts.csv", index=False)
    print("Wrote data/portfolio_facts.csv (Power BI source)")

    # ---- automated Excel report ----
    summary = pd.DataFrame({
        "Metric": ["Annualised return", "Annualised volatility", "Sharpe ratio", "Max drawdown"],
        "Value": [f"{port_ann_return:.2%}", f"{port_ann_vol:.2%}", f"{port_sharpe:.2f}", f"{max_dd:.2%}"],
    })
    xlsx = HERE / "reports" / "portfolio_report.xlsx"
    with pd.ExcelWriter(xlsx, engine="openpyxl") as xl:
        summary.to_excel(xl, sheet_name="Summary", index=False)
        per_asset.to_excel(xl, sheet_name="PerAsset", index=False)
        daily_ret.corr().round(2).to_excel(xl, sheet_name="Correlation")
        port_cum.rename("PortfolioValue").to_frame().to_excel(xl, sheet_name="GrowthOf1")
    print(f"Wrote {xlsx}")

    # ---- interactive Plotly dashboard ----
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Growth of 1€ invested", "Allocation", "Risk vs Return by asset", "Max drawdown"),
        specs=[[{"type": "scatter"}, {"type": "domain"}], [{"type": "scatter"}, {"type": "scatter"}]],
    )
    fig.add_trace(go.Scatter(x=port_cum.index, y=port_cum.values, name="Portfolio",
                             line=dict(color="#38bdf8")), row=1, col=1)
    fig.add_trace(go.Pie(labels=list(weights.index), values=list(weights.values), hole=0.5), row=1, col=2)
    fig.add_trace(go.Scatter(x=per_asset["AnnVolatility"], y=per_asset["AnnReturn"], mode="markers+text",
                             text=per_asset["Ticker"], textposition="top center",
                             marker=dict(size=14, color="#f59e0b")), row=2, col=1)
    fig.add_trace(go.Scatter(x=drawdown.index, y=drawdown.values, fill="tozeroy",
                             line=dict(color="#f87171"), name="Drawdown"), row=2, col=2)
    fig.update_layout(template="plotly_dark", showlegend=False, height=760,
                      title_text="Investment Portfolio — Immersive Analytics Dashboard")
    fig.update_xaxes(title_text="Volatility", row=2, col=1)
    fig.update_yaxes(title_text="Return", row=2, col=1)
    out_html = HERE / "dashboard" / "portfolio_dashboard.html"
    fig.write_html(out_html)
    print(f"Wrote {out_html}")


if __name__ == "__main__":
    main()
