# LaunchTower Factor Model Report — 2026-09-16

**Universe:** 151 US large-caps · **Window:** trailing 252 trading days (2024-09-16 → 2026-09-11) · **Data:** yfinance, split/dividend-adjusted closes · **Model:** 50% Momentum (12m return z-score) + 50% Quality (−volatility z-score)

> **Disclaimer:** Research/educational output from public market data. Not personalized investment advice; not a recommendation to buy or sell any security. Past performance does not guarantee future results.

---

## Method (reproducible in ~15 lines)

1. Pull 2 years of adjusted daily closes for 151 tickers.
2. Per ticker, over the last 252 sessions compute: `ret_1m/3m/6m/12m`, annualized realized vol, max drawdown, distance from 52w high.
3. Cross-sectionally z-score `ret_12m` → **Momentum**; z-score `vol_ann` and negate → **Quality**.
4. **Composite = 0.5·Momentum + 0.5·Quality**, rank 1–151.

Full code: `launchtower_factor_screen_2026-09-16.py` (in this repo).

---

## Top 10 (highest composite)

| # | Ticker | Last | 12m Ret | Vol (ann) | From 52w High | Momentum | Quality | Composite |
|---|--------|------|---------|-----------|---------------|----------|---------|-----------|
| 1 | **MU** | 975.26 | +548.8% | 81.4% | −19.6% | +6.55 | −2.14 | **+2.204** |
| 2 | **VLO** | 390.42 | +153.0% | 36.2% | 0.0% | +1.52 | +0.13 | **+0.825** |
| 3 | **INTC** | 102.94 | +318.3% | 79.7% | −27.0% | +3.62 | −2.05 | **+0.786** |
| 4 | **MPC** | 395.93 | +120.8% | 34.3% | −0.9% | +1.12 | +0.22 | **+0.669** |
| 5 | **PSX** | 259.47 | +101.6% | 30.9% | −0.5% | +0.87 | +0.39 | **+0.630** |
| 6 | **JNJ** | 265.58 | +52.1% | 19.2% | −4.6% | +0.24 | +0.98 | **+0.611** |
| 7 | **CSX** | 48.95 | +50.9% | 22.2% | −7.8% | +0.23 | +0.82 | **+0.526** |
| 8 | **TTE** | 91.89 | +56.1% | 24.6% | −1.8% | +0.29 | +0.70 | **+0.499** |
| 9 | **TGT** | 155.83 | +77.2% | 30.6% | −8.3% | +0.56 | +0.40 | **+0.482** |
| 10 | **TRV** | 375.20 | +36.3% | 20.8% | −5.2% | +0.04 | +0.89 | **+0.469** |

## Bottom 10 (lowest composite)

| # | Ticker | Last | 12m Ret | Vol (ann) | From 52w High | Momentum | Quality | Composite |
|---|--------|------|---------|-----------|---------------|----------|---------|-----------|
| 142 | PLTR | 167.23 | +1.8% | 60.9% | −19.3% | −0.40 | −1.11 | −0.753 |
| 143 | INTU | 321.57 | −50.8% | 48.7% | −53.7% | −1.06 | −0.50 | −0.781 |
| 144 | SE | 106.24 | −45.9% | 50.8% | −45.9% | −1.00 | −0.61 | −0.804 |
| 145 | NOW | 132.53 | −29.4% | 56.9% | −31.1% | −0.79 | −0.91 | −0.850 |
| 146 | ORCL | 150.28 | −50.6% | 57.0% | −53.7% | −1.06 | −0.92 | −0.989 |
| 147 | HOOD | 112.57 | −4.4% | 72.2% | −26.2% | −0.47 | −1.68 | −1.075 |
| 148 | ZS | 164.54 | −42.6% | 63.2% | −51.1% | −0.96 | −1.23 | −1.092 |
| 149 | MRNA | 143.97 | +467.0% | 192.6% | −17.4% | +5.51 | −7.70 | −1.095 |
| 150 | COIN | 175.26 | −45.9% | 70.8% | −54.7% | −1.00 | −1.61 | −1.303 |
| 151 | **SMCI** | 40.10 | −8.8% | 91.6% | −31.7% | −0.53 | −2.65 | **−1.587** |

---

## What the screen is saying (2026-09-16)

- **Memory is the momentum story of the year.** MU leads the entire 151-stock universe with a +549% trailing-12m return (HBM cycle), followed by INTC (+318%) and AMD (+232%). The model's momentum leg is doing the heavy lifting on the top of the table.
- **Refiners are the quality story.** VLO, MPC, PSX all sit in the top 5 with low volatility (31–36% ann), near 52w highs, and double-digit 12m returns — the classic "earnings beat + low vol" profile the quality leg rewards.
- **Defensives are quietly ranking well.** JNJ (#6), CSX (#7), TTE (#8), TRV (#10) all combine modest positive momentum with the lowest vol in the universe — the model's natural hedge sleeve.
- **The bottom of the table is a software/fintech cluster.** ORCL, NOW, INTU, ZS, PLTR all show deep 52w drawdowns (−19% to −54%) combined with elevated vol — the model is flagging them as both weak momentum and poor quality.
- **MRNA is a data outlier to watch:** +467% 12m return but 193% annualized vol pushes its quality score to −7.7, dragging it to #149. The composite is doing exactly what it's designed to do — penalizing lottery-ticket vol.
- **SMCI is the bottom of the universe** on both legs (−0.53 momentum, −2.65 quality) — the model's clearest "avoid" signal this screen.

---

## Files in this repo

| File | What it is |
|------|------------|
| `launchtower_factor_report_2026-09-16.md` | This report |
| `launchtower_signal_2026-09-16.csv` | Full 151-row factor table (all raw factors + z-scores + composite) |
| `launchtower_factor_screen_2026-09-16.py` | The complete, runnable script that reproduces every number above |

**How to reproduce:**
```bash
pip install yfinance pandas numpy
python launchtower_factor_screen_2026-09-16.py
```

---

*LaunchTower — independent market-data desk. This report is regenerated from live public data; numbers reflect the close of the last trading session available at generation time.*
