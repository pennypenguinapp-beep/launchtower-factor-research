# LaunchTower — Factor Screen (Free Sample)

> **Independent market-data desk.** We build reproducible, documented factor screens on US large-caps from public market data. This repo is the **free sample** — the full dataset, methodology pack, and live signal feed are available on [Whop](https://whop.com).

> ⚠️ **Disclaimer:** Research/educational output from public market data. **Not** personalized investment advice, **not** a recommendation to buy or sell any security. Past performance does not guarantee future results.

---

## What's in this repo

| File | Description |
|------|-------------|
| `launchtower_factor_report_2026-09-16.md` | Dated research report: top/bottom 10, factor scores, narrative |
| `launchtower_signal_2026-09-16.csv` | Full 151-row factor table (raw factors + z-scores + composite) |
| `launchtower_factor_screen_2026-09-16.py` | The complete, runnable script that reproduces every number |

## The model in one paragraph

Pull 2 years of split/dividend-adjusted daily closes for **151 US large-caps**. Over the trailing 252 trading days, compute per-ticker: 1m/3m/6m/12m returns, annualized realized volatility, max drawdown, distance from 52w high. Cross-sectionally z-score the 12m return → **Momentum**; z-score annualized vol and negate → **Quality**. **Composite = 0.5·Momentum + 0.5·Quality**, rank 1–151.

## How to run it yourself

```bash
pip install yfinance pandas numpy
python launchtower_factor_screen_2026-09-16.py
```

The script prints the top/bottom 10 and writes a dated CSV of the full factor table.

## Latest screen (2026-09-16)

**Top 5:** MU · VLO · INTC · MPC · PSX
**Bottom 5:** HOOD · ZS · MRNA · COIN · SMCI

Full table: see the CSV. Narrative: see the report.

## What's in the paid pack (Whop)

- Full 151-ticker dataset with all raw factors, z-scores, and composite scores
- Complete methodology documentation (factor definitions, z-scoring, weighting, edge cases)
- Live signal feed (dated CSV, updated on a schedule)
- The full runnable script with configuration knobs (universe, window, weights)

👉 **[Get the full pack on Whop](https://whop.com)**

---

*LaunchTower — independent market-data desk. Data: yfinance (public). Regenerated from live data at generation time.*
