# LaunchTower Weekly Momentum Signal — 2026-09-16 (data through 2026-09-11)

**Universe:** 153 US large-cap equities
**Data window:** 2024-09-12 → 2026-09-11 (501 trading days)
**Source:** Yahoo Finance (auto-adjusted daily closes)
**Model:** 5-factor momentum + quality composite (0–100 percentile scale)

## Model weights

| Factor | Weight | Direction |
|---|---|---|
| 6-month return | 35% | higher = better |
| 3-month return | 20% | higher = better |
| Annualized volatility | 20% | lower = better |
| Max drawdown (12M) | 15% | shallower = better |
| Distance from 52w high | 10% | closer = better |

Each factor is percentile-ranked within the universe, then weighted. No look-ahead: every factor uses only trailing data.

## Top 10 — Highest Composite Score

| rank | ticker | name | 6M ret | 12M ret | ann vol |
|---:|:---|:---|---:|---:|---:|
| 1 | MRNA | Moderna | 169.7% | 492.2% | 192.2% |
| 2 | TEAM | Atlassian | 145.0% | 3.1% | 77.7% |
| 3 | TGT | Target | 36.9% | 78.6% | 30.6% |
| 4 | PYPL | PayPal | 21.8% | -17.2% | 44.1% |
| 5 | PANW | Palo Alto Networks | 96.7% | 67.6% | 45.3% |
| 6 | SNOW | Snowflake | 85.6% | 45.7% | 65.3% |
| 7 | OKTA | Okta | 110.9% | 84.6% | 64.5% |
| 8 | HOOD | Robinhood | 47.9% | -4.2% | 72.0% |
| 9 | DASH | DoorDash | 24.9% | -21.6% | 47.5% |
| 10 | ABNB | Airbnb | 33.3% | 37.9% | 34.8% |

## Bottom 5 — Lowest Composite Score

| rank | ticker | name |
|---:|:---|:---|
| 149 | BIDU | Baidu |
| 150 | LCID | Lucid Group |
| 151 | NIO | NIO |
| 152 | APP | AppLovin |
| 153 | RARE | Ultragenyx |

## What this is NOT

- Not financial advice. Not a recommendation to buy or sell any security.
- No return or performance guarantee. Past factor rankings do not predict future returns.
- The universe is large-cap US equities only; small/mid caps, non-US, crypto, and fixed income are excluded.

## What you get (subscription)

- **Weekly CSV** (153 rows × 14 columns) delivered every Friday after market close.
- **Full methodology** (this README) — reproducible, no black box.
- **Raw factor table** — every intermediate score, so you can re-weight or backtest yourself.
- **Change log** — which tickers moved in/out of the top 20 vs. last week, with the delta.

## Disclaimer

LaunchTower is a research tool, not a broker, advisor, or investment fund. Data is provided "as is" from public sources; no warranty of accuracy or fitness for a particular purpose. Consult a licensed financial advisor before acting on any data.
