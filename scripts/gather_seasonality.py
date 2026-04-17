#!/usr/bin/env python3
"""
gather_seasonality.py — Google Trends via pytrends.

For each country, pulls 5-year weekly interest-over-time for a generic travel
query ("{country} tickets" or "{country} attractions"), scoped to the 6 GCC
origins combined. Derives:
  - seasonalityCurve (12-element monthly avg, peak=100)
  - peakMonth / troughMonth
  - yoyGrowthPct (last 12mo vs prior 12mo)
  - 5yrTrendSlope (linear regression slope on monthly aggregates)

Output: data/seasonality.json

Rate limit: pytrends gets IP-blocked aggressively. Uses long sleeps + fallback.
If a market fails, it's logged and skipped (user's guidance: drop what blocks).
"""
import json
import time
from pathlib import Path

# --- pytrends + urllib3 v2 compat shim ---
# pytrends passes `method_whitelist=` to urllib3.Retry; renamed to `allowed_methods` in v2.
import urllib3.util.retry as _retry
_orig_retry_init = _retry.Retry.__init__
def _patched_init(self, *args, **kwargs):
    if "method_whitelist" in kwargs:
        kwargs["allowed_methods"] = kwargs.pop("method_whitelist")
    _orig_retry_init(self, *args, **kwargs)
_retry.Retry.__init__ = _patched_init
# -----------------------------------------

from pytrends.request import TrendReq

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "data" / "seasonality.json"

# 6 GCC ISO codes (UAE, KSA, Kuwait, Qatar, Oman, Bahrain)
# pytrends geo param takes ONE code at a time. We'll use UAE as primary proxy
# (largest GCC online population, best signal-to-noise) and note it in output.
GEO = "AE"
TIMEFRAME = "today 5-y"

QUERIES = {
    "Italy": "italy tickets",
    "Spain": "spain attractions",
    "Greece": "greece tickets",
    "Portugal": "portugal tickets",
    "Austria": "austria tickets",
    "Germany": "germany tickets",
    "Netherlands": "amsterdam tickets",
    "Ireland": "ireland tickets",
    "France": "paris tickets",
    "United Kingdom": "london tickets",
    "Switzerland": "switzerland tickets",
    "Czech Republic": "prague tickets",
    "Poland": "poland tickets",
    "Hungary": "budapest tickets",
    "Turkey": "istanbul tickets",
    "Egypt": "egypt tickets",
    "Jordan": "jordan tickets",
    "Morocco": "morocco tickets",
    "Malaysia": "malaysia tickets",
    "Singapore": "singapore tickets",
    "Japan": "japan tickets",
    "Thailand": "thailand tickets",
    "Indonesia": "bali tickets",
    "Vietnam": "vietnam tickets",
}


def derive(weekly_df, country: str, query: str) -> dict:
    """Collapse weekly to monthly, compute seasonality + YoY + trend."""
    if weekly_df is None or weekly_df.empty or query not in weekly_df.columns:
        return {"error": "no data"}

    s = weekly_df[query]
    # monthly mean
    monthly = s.resample("ME").mean().dropna()
    if len(monthly) < 24:
        return {"error": f"only {len(monthly)} months"}

    by_month = {m: [] for m in range(1, 13)}
    for ts, v in monthly.items():
        by_month[ts.month].append(v)
    avg_by_month = [sum(by_month[m]) / len(by_month[m]) if by_month[m] else 0 for m in range(1, 13)]
    peak = max(avg_by_month) or 1
    curve = [round(v / peak * 100, 1) for v in avg_by_month]
    peak_month = avg_by_month.index(peak) + 1
    pos = [v for v in avg_by_month if v > 0]
    trough_month = avg_by_month.index(min(pos)) + 1 if pos else None

    last12 = monthly.iloc[-12:].mean()
    prior12 = monthly.iloc[-24:-12].mean()
    yoy = ((last12 - prior12) / prior12 * 100.0) if prior12 else None

    # simple trend: slope of monthly over full 5y series
    import numpy as np
    x = np.arange(len(monthly))
    y = monthly.values
    slope = float(np.polyfit(x, y, 1)[0]) if len(y) >= 4 else None

    return {
        "query": query,
        "geo": GEO,
        "seasonalityCurve": curve,
        "peakMonth": peak_month,
        "troughMonth": trough_month,
        "yoyGrowthPct": round(float(yoy), 1) if yoy is not None else None,
        "trendSlope5y": round(slope, 4) if slope is not None else None,
        "monthsAvailable": len(monthly),
    }


def main() -> int:
    pytrends = TrendReq(hl="en-US", tz=0, retries=2, backoff_factor=1.0, timeout=(10, 30))
    result = {}
    fails = []

    for i, (country, query) in enumerate(QUERIES.items()):
        print(f"[{i+1}/{len(QUERIES)}] {country:20s} '{query}' ...", end=" ", flush=True)
        try:
            pytrends.build_payload([query], timeframe=TIMEFRAME, geo=GEO)
            df = pytrends.interest_over_time()
            derived = derive(df, country, query)
            if "error" in derived:
                print(f"! {derived['error']}")
                fails.append((country, derived["error"]))
                continue
            result[country] = derived
            print(f"peak={derived['peakMonth']:02d} YoY={derived['yoyGrowthPct']}")
        except Exception as e:
            msg = str(e)[:80]
            print(f"!! {msg}")
            fails.append((country, msg))
        time.sleep(3)  # polite; Google throttles aggressively

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump({
            "_source": "Google Trends (pytrends)",
            "_geo": GEO,
            "_timeframe": TIMEFRAME,
            "_note": "Geo=AE used as GCC proxy (pytrends doesn't support multi-geo union). UAE is the largest GCC online population.",
            "_failures": fails,
            "data": result,
        }, f, indent=2)

    print(f"\n✓ wrote {OUTPUT_FILE}")
    print(f"  {len(result)} countries ok · {len(fails)} failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
