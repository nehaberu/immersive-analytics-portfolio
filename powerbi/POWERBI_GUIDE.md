# Building the Power BI dashboard

A `.pbix` file can't be generated from code, so this guide lets you build the Power BI
dashboard yourself in ~20 minutes from the data this project produces. (The Python/Plotly
dashboard in `dashboard/` shows the same analysis as a runnable reference.)

## 1. Load the data
1. Open **Power BI Desktop** → *Home → Get Data → Text/CSV*.
2. Load `data/portfolio_facts.csv` (columns: Date, Ticker, Open, High, Low, Close, Volume, Weight).
3. In *Power Query*, set `Date` to **Date** type and the price columns to **Decimal number**, then *Close & Apply*.

## 2. Create a Date table (for time intelligence)
In *Modeling → New Table*:
```DAX
DateTable = CALENDAR ( MIN ( portfolio_facts[Date] ), MAX ( portfolio_facts[Date] ) )
```
Mark it as a date table and relate `DateTable[Date]` → `portfolio_facts[Date]`.

## 3. DAX measures (Modeling → New Measure)
```DAX
Total Volume   = SUM ( portfolio_facts[Volume] )

Latest Close   = CALCULATE ( AVERAGE ( portfolio_facts[Close] ),
                             LASTDATE ( portfolio_facts[Date] ) )

-- Daily return per ticker (uses previous trading day's close)
Daily Return =
VAR PrevClose =
    CALCULATE ( AVERAGE ( portfolio_facts[Close] ),
                DATEADD ( DateTable[Date], -1, DAY ) )
RETURN DIVIDE ( AVERAGE ( portfolio_facts[Close] ) - PrevClose, PrevClose )

-- Weighted contribution of each holding
Weighted Close = SUMX ( portfolio_facts,
                        portfolio_facts[Close] * portfolio_facts[Weight] )
```

## 4. Visuals to add
| Visual | Fields |
|--------|--------|
| **Line chart** | Axis: `DateTable[Date]`, Values: `Latest Close`, Legend: `Ticker` |
| **Donut** | Legend: `Ticker`, Values: `Weight` (allocation) |
| **Scatter** | X: volatility measure, Y: return measure, details: `Ticker` |
| **Cards** | `Latest Close`, `Total Volume` |
| **Slicer** | `Ticker` and a `DateTable[Date]` range |

## 5. Save as `portfolio.pbix` in this folder and (optionally) export a PDF/PNG to `reports/`.

---
**Talking point:** *"I built the central dataset in Python, exported a clean fact table,
then modelled it in Power BI with a date table and DAX measures for returns and weighted
exposure, and built an interactive dashboard with slicers for ticker and time period."*
