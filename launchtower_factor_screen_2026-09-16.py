#!/usr/bin/env python3
"""
LaunchTower — Momentum + Quality Factor Screen
==============================================

A complete, self-contained, reproducible factor screen for a universe of
151 US large-caps.

WHAT IT DOES
------------
1. Downloads ~2 years of split/dividend-adjusted daily closes via `yfinance`.
2. Computes factors per ticker over a trailing 12-month (252 trading day) window:
     - ret_1m / ret_3m / ret_6m / ret_12m : total returns
     - vol_ann   : 12-month annualized realized volatility
     - maxdd     : 12-month maximum drawdown
     - from_high : distance from 52-week high
3. Z-scores every factor cross-sectionally (mean 0, std 1 across the universe).
4. Builds:
     - Momentum  = z-score of 12-month return
     - Quality   = negative z-score of annualized volatility
     - Composite = 0.5 * Momentum + 0.5 * Quality
5. Prints the TOP 10 and BOTTOM 10 tickers by composite score, and writes a
   dated CSV of the full factor table to the current directory.

REQUIREMENTS
------------
    pip install yfinance pandas numpy

DISCLAIMER
----------
Research / educational tool built from public market data. This is NOT
personalized investment advice and is not a recommendation to buy or sell
any security. Run at your own risk.

LaunchTower — independent market-data desk.
"""

from __future__ import annotations

import sys
import datetime as dt

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "ERROR: the 'yfinance' package is required.\n"
        "Install it with:  pip install yfinance\n"
    )
    raise

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

UNIVERSE = [
    "AAPL","MSFT","NVDA","GOOGL","AMZN","META","TSLA","AVGO","AMD","NFLX","ORCL","CRM","ADBE","CSCO","QCOM","TXN","MU","INTC","IBM","NOW","INTU","PLTR","SNOW","DDOG","NET","CRWD","PANW","ZS","FTNT","ANET","SMCI","ARM","MRVL","LRCX","AMAT","KLAC","ASML","ON","MPWR","MCHP","TER","ADSK","CDNS","SNPS","GFS","MRNA","LLY","NVO","UNH","JNJ","PFE","MRK","ABBV","BMY","TMO","DHR","ISRG","VRTX","REGN","AMGN","GILD","BSX","CVS","CI","HUM","ABT","SYK","ALGN","MDT","BABA","JD","PDD","SE","BIDU","UBER","ABNB","DASH","COIN","HOOD","PYPL","V","MA","AXP","BLK","SCHW","C","BAC","WFC","JPM","GS","MS","SPGI","ICE","CME","MCO","AIG","MET","PRU","TRV","ALL","CB","PGR","SPOT","T","VZ","TMUS","CMCSA","DIS","WMT","COST","HD","MCD","NKE","SBUX","TGT","UPS","CAT","DE","GE","BA","HON","UNP","CSX","NSC","LIN","APD","ECL","SHW","EMR","ETN","PH","ROK","WM","RSG","COP","XOM","CVX","SLB","OXY","EOG","DVN","PSX","VLO","MPC","PBR","BP","SHEL","TTE","RIO","FCX","NEM"
]

TRADING_DAYS = 252
TOP_N = 10


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def fetch_closes(tickers: list[str]) -> tuple[pd.DataFrame, list[str]]:
    """
    Download adjusted close prices for all tickers.

    Returns
    -------
    (closes, dropped)
        closes : DataFrame indexed by date, one column per valid ticker
        dropped: list of tickers that returned no usable data
    """
    end = dt.datetime.now()
    start = end - dt.timedelta(days=730)

    print(f"Downloading {len(tickers)} tickers via yfinance ...")

    data = yf.download(
        tickers,
        start=start.strftime('%Y-%m-%d'),
        end=end.strftime('%Y-%m-%d'),
        auto_adjust=True,
        group_by="ticker",
        threads=True,
        progress=False,
    )

    if data is None or data.empty:
        raise RuntimeError("yfinance returned no data for any ticker.")

    closes = pd.DataFrame(index=data.index)
    dropped = []

    for t in tickers:
        try:
            if isinstance(data.columns, pd.MultiIndex):
                series = data[t]["Close"]
            else:
                series = data["Close"]
        except (KeyError, TypeError):
            dropped.append(t)
            continue

        series = series.dropna()
        if len(series) < TRADING_DAYS:
            dropped.append(t)
            continue
        closes[t] = series

    closes = closes.dropna(how="all")
    return closes, dropped


# ---------------------------------------------------------------------------
# Factor math
# ---------------------------------------------------------------------------

def _max_drawdown(prices: pd.Series) -> float:
    """Maximum drawdown (negative number) over the given price path."""
    prices = prices.dropna()
    if len(prices) < 2:
        return 0.0
    running_max = prices.cummax()
    drawdown = prices / running_max - 1.0
    return float(drawdown.min())


def _zscore(s: pd.Series) -> pd.Series:
    """Cross-sectional z-score; guard against zero std."""
    m = s.mean()
    sd = s.std()
    if pd.isna(sd) or sd == 0:
        return pd.Series(0.0, index=s.index)
    return (s - m) / sd


def compute_factors(closes: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the raw factors for each ticker over the trailing 12m window.
    """
    rows = []
    for t in closes.columns:
        px = closes[t].dropna()
        if len(px) < TRADING_DAYS:
            continue
        window = px.iloc[-TRADING_DAYS:]
        last = float(px.iloc[-1])

        ret_1m = last / float(px.iloc[-22]) - 1.0
        ret_3m = last / float(px.iloc[-64]) - 1.0
        ret_6m = last / float(px.iloc[-127]) - 1.0
        ret_12m = last / float(window.iloc[0]) - 1.0

        daily_ret = window.pct_change().dropna()
        vol_ann = float(daily_ret.std(ddof=1) * np.sqrt(TRADING_DAYS))
        maxdd = _max_drawdown(window)

        high_52w = float(window.max())
        from_high = last / high_52w - 1.0

        rows.append({
            "ticker": t,
            "last_price": last,
            "ret_1m": ret_1m,
            "ret_3m": ret_3m,
            "ret_6m": ret_6m,
            "ret_12m": ret_12m,
            "vol_ann": vol_ann,
            "max_drawdown": maxdd,
            "from_52w_high": from_high,
        })

    if not rows:
        raise RuntimeError("No ticker had enough price history to compute factors.")

    return pd.DataFrame(rows).set_index("ticker").sort_index()


def build_scores(factors: pd.DataFrame) -> pd.DataFrame:
    """
    Z-score the factors cross-sectionally and build momentum / quality / composite.
    """
    mom_z = _zscore(factors["ret_12m"])
    vol_z = _zscore(factors["vol_ann"])

    momentum = mom_z
    quality = -vol_z
    composite = 0.5 * momentum + 0.5 * quality

    out = factors.copy()
    out["momentum_score"] = momentum.round(4)
    out["quality_score"] = quality.round(4)
    out["composite_score"] = composite.round(4)
    out = out.sort_values("composite_score", ascending=False)
    out.insert(0, "rank", range(1, len(out) + 1))
    out.insert(1, "date", dt.date.today().isoformat())
    return out.reset_index()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    closes, dropped = fetch_closes(UNIVERSE)
    if dropped:
        print(f"  (dropped {len(dropped)} tickers with insufficient data: {dropped})")
    print(f"  Valid tickers: {len(closes.columns)}")
    print(f"  Date range: {closes.index.min().date()} → {closes.index.max().date()}")

    factors = compute_factors(closes)
    scores = build_scores(factors)

    print(f"\n{'='*70}")
    print(f"  TOP {TOP_N} by composite score")
    print(f"{'='*70}")
    top = scores.head(TOP_N)[
        ["rank","ticker","last_price","ret_12m","vol_ann","from_52w_high",
         "momentum_score","quality_score","composite_score"]
    ]
    print(top.to_string(index=False))

    print(f"\n{'='*70}")
    print(f"  BOTTOM {TOP_N} by composite score")
    print(f"{'='*70}")
    bottom = scores.tail(TOP_N)[
        ["rank","ticker","last_price","ret_12m","vol_ann","from_52w_high",
         "momentum_score","quality_score","composite_score"]
    ]
    print(bottom.to_string(index=False))

    out_path = f"launchtower_signal_{dt.date.today().isoformat()}.csv"
    scores.to_csv(out_path, index=False)
    print(f"\nWrote full factor table → {out_path}  ({len(scores)} rows)")


if __name__ == "__main__":
    main()
