"""
Generate synthetic daily stock-price data for a small investment portfolio.

This stands in for a Kaggle stock-prices dataset so the project runs with zero setup.
The shape (Date, Ticker, Open/High/Low/Close, Volume) matches common Kaggle stock
datasets, so you can later drop in the real CSVs and everything downstream still works.

  Real data option (e.g. Kaggle "S&P 500 stock data" / "Huge Stock Market Dataset"):
  put per-ticker CSVs in data/raw/ with columns Date,Open,High,Low,Close,Volume and
  point build_portfolio.py at them instead.

Run:  python data/generate_data.py
Output: data/prices.csv  (long format: one row per ticker per day)
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(7)

# ticker -> (start price, annual drift, annual volatility)
TICKERS = {
    "AAPL": (150, 0.18, 0.28),
    "MSFT": (250, 0.16, 0.25),
    "AMZN": (120, 0.14, 0.33),
    "JPM":  (140, 0.09, 0.22),
    "KO":   (55,  0.06, 0.15),   # defensive, low vol
    "XOM":  (95,  0.07, 0.27),
}

START = "2021-01-01"
END = "2024-12-31"


def simulate(start_price, mu, sigma, dates):
    """Geometric Brownian Motion -> a realistic price path."""
    n = len(dates)
    dt = 1 / 252                                   # trading days per year
    shocks = RNG.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), n)
    price = start_price * np.exp(np.cumsum(shocks))
    return price


def main():
    dates = pd.bdate_range(START, END)             # business days only
    frames = []
    for ticker, (p0, mu, sigma) in TICKERS.items():
        close = simulate(p0, mu, sigma, dates)
        daily = pd.DataFrame({
            "Date": dates,
            "Ticker": ticker,
            "Close": np.round(close, 2),
        })
        # derive plausible OHLC + volume around the close
        daily["Open"]   = np.round(close * RNG.uniform(0.99, 1.01, len(dates)), 2)
        daily["High"]   = np.round(daily[["Open", "Close"]].max(axis=1) * RNG.uniform(1.0, 1.02, len(dates)), 2)
        daily["Low"]    = np.round(daily[["Open", "Close"]].min(axis=1) * RNG.uniform(0.98, 1.0, len(dates)), 2)
        daily["Volume"] = RNG.integers(2_000_000, 40_000_000, len(dates))
        frames.append(daily)

    out = pd.concat(frames, ignore_index=True)[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]]
    out.to_csv("data/prices.csv", index=False)
    print(f"Wrote {len(out)} rows ({len(TICKERS)} tickers x {len(dates)} days) -> data/prices.csv")


if __name__ == "__main__":
    main()
