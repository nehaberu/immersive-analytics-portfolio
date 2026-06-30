"""
Load REAL financial data from Kaggle into the project's price format.

Dataset: "S&P 500 stock data"  (Kaggle, by camnugent)
  https://www.kaggle.com/datasets/camnugent/sandp500
  File needed: all_stocks_5yr.csv   (columns: date, open, high, low, close, volume, Name)

How to get the file (free Kaggle account):
  Option A - manual:  download all_stocks_5yr.csv from the page above and put it in
                      this `data/` folder.
  Option B - Kaggle API (if installed & configured with ~/.kaggle/kaggle.json):
                      kaggle datasets download -d camnugent/sandp500 -f all_stocks_5yr.csv -p data --unzip

Then run:  python data/load_kaggle.py
Output:    data/prices.csv   (same format the rest of the pipeline expects)

This script filters the big file down to a few tickers and an optional date range
("cut it short"), so the project runs on a small, real dataset.
"""

from pathlib import Path
import sys
import pandas as pd

HERE = Path(__file__).parent
RAW = HERE / "all_stocks_5yr.csv"

# Pick the portfolio tickers (these all exist in the S&P 500 dataset) and a date
# window to keep the dataset small. Change these freely.
TICKERS = ["AAPL", "MSFT", "AMZN", "JPM", "KO", "XOM"]
START = "2015-01-01"        # cut it short: keep ~3 years instead of 5
END = "2018-12-31"


def main():
    if not RAW.exists():
        sys.exit(f"ERROR: {RAW} not found.\n"
                 f"Download all_stocks_5yr.csv from "
                 f"https://www.kaggle.com/datasets/camnugent/sandp500 into the data/ folder "
                 f"(see instructions at the top of this file).")

    df = pd.read_csv(RAW, parse_dates=["date"])
    df = df[df["Name"].isin(TICKERS)]
    df = df[(df["date"] >= START) & (df["date"] <= END)]

    # rename to the project's expected schema
    df = df.rename(columns={
        "date": "Date", "Name": "Ticker", "open": "Open", "high": "High",
        "low": "Low", "close": "Close", "volume": "Volume",
    })
    df = df[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
    df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)

    out = HERE / "prices.csv"
    df.to_csv(out, index=False)
    found = sorted(df["Ticker"].unique())
    print(f"Wrote {len(df)} rows ({len(found)} tickers: {', '.join(found)}) "
          f"from {df['Date'].min().date()} to {df['Date'].max().date()} -> {out}")
    missing = set(TICKERS) - set(found)
    if missing:
        print(f"NOTE: these requested tickers were not in the file: {', '.join(sorted(missing))}")


if __name__ == "__main__":
    main()
