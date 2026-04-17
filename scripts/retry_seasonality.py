#!/usr/bin/env python3
"""Retry pass for markets that 429'd in gather_seasonality.py.

Reads data/seasonality.json, retries only failed countries with:
  - fresh TrendReq client each time
  - 20s sleep between requests
  - fallback query variants if first attempt fails
"""
import json
import time
import random
from pathlib import Path

# urllib3 v2 compat shim
import urllib3.util.retry as _retry
_orig_retry_init = _retry.Retry.__init__
def _patched_init(self, *args, **kwargs):
    if "method_whitelist" in kwargs:
        kwargs["allowed_methods"] = kwargs.pop("method_whitelist")
    _orig_retry_init(self, *args, **kwargs)
_retry.Retry.__init__ = _patched_init

from pytrends.request import TrendReq

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "data" / "seasonality.json"
GEO = "AE"
TIMEFRAME = "today 5-y"

# Fallback variants — if primary query fails, try these in order
FALLBACKS = {
    "Netherlands": ["netherlands tickets", "holland tickets", "amsterdam attractions"],
    "Ireland": ["ireland tickets", "dublin tickets", "ireland attractions"],
    "Switzerland": ["switzerland tickets", "zurich tickets", "swiss attractions"],
    "Czech Republic": ["prague tickets", "czech republic tickets", "prague attractions"],
    "Poland": ["poland tickets", "krakow tickets", "warsaw tickets"],
    "Hungary": ["budapest tickets", "hungary tickets", "budapest attractions"],
    "Turkey": ["istanbul tickets", "turkey tickets", "cappadocia tickets"],
    "Egypt": ["egypt tickets", "cairo tickets", "pyramids tickets"],
    "Jordan": ["jordan tickets", "petra tickets", "jordan attractions"],
    "Thailand": ["thailand tickets", "bangkok tickets", "phuket tickets"],
}


def derive(weekly_df, query):
    if weekly_df is None or weekly_df.empty or query not in weekly_df.columns:
        return None
    s = weekly_df[query]
    monthly = s.resample("ME").mean().dropna()
    if len(monthly) < 24:
        return None
    by_month = {m: [] for m in range(1, 13)}
    for ts, v in monthly.items():
        by_month[ts.month].append(v)
    avg = [sum(by_month[m]) / len(by_month[m]) if by_month[m] else 0 for m in range(1, 13)]
    peak = max(avg) or 1
    curve = [round(v / peak * 100, 1) for v in avg]
    pos = [v for v in avg if v > 0]
    last12 = monthly.iloc[-12:].mean()
    prior12 = monthly.iloc[-24:-12].mean()
    yoy = ((last12 - prior12) / prior12 * 100.0) if prior12 else None
    import numpy as np
    slope = float(np.polyfit(range(len(monthly)), monthly.values, 1)[0])
    return {
        "query": query,
        "geo": GEO,
        "seasonalityCurve": curve,
        "peakMonth": avg.index(peak) + 1,
        "troughMonth": avg.index(min(pos)) + 1 if pos else None,
        "yoyGrowthPct": round(float(yoy), 1) if yoy is not None else None,
        "trendSlope5y": round(slope, 4),
        "monthsAvailable": len(monthly),
    }


def main():
    with open(OUTPUT_FILE) as f:
        state = json.load(f)

    failed = [f[0] for f in state["_failures"]]
    print(f"Retrying {len(failed)} markets: {failed}\n")

    still_failed = []
    for i, country in enumerate(failed):
        variants = FALLBACKS.get(country, [country.lower() + " tickets"])
        print(f"[{i+1}/{len(failed)}] {country}")
        success = None
        for variant in variants:
            try:
                pyt = TrendReq(hl="en-US", tz=0, retries=3, backoff_factor=2.0, timeout=(15, 45))
                pyt.build_payload([variant], timeframe=TIMEFRAME, geo=GEO)
                df = pyt.interest_over_time()
                d = derive(df, variant)
                if d:
                    print(f"    ✓ '{variant}' peak={d['peakMonth']:02d} YoY={d['yoyGrowthPct']}")
                    success = d
                    break
                print(f"    ~ '{variant}' no data")
            except Exception as e:
                print(f"    ! '{variant}' {str(e)[:60]}")
            time.sleep(20 + random.random() * 10)

        if success:
            state["data"][country] = success
        else:
            still_failed.append((country, "all variants failed"))
        time.sleep(15 + random.random() * 10)

    state["_failures"] = still_failed
    with open(OUTPUT_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print(f"\n✓ {len(state['data'])} countries now have data · {len(still_failed)} still failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
