#!/usr/bin/env python3
"""
gather_landmarks.py — Wikipedia Pageviews API.

Pulls monthly pageviews (last 36 months) for each landmark in landmarks.json.
Output: data/landmarks_pageviews.json

- Free, no auth.
- Rate limit: 100 req/s. We stay well under.
- One HTTP call per (landmark, 36-month window).

Derived signals emitted into output:
  - annualPageviews (sum of last 12 complete months)
  - yoyGrowthPct (last 12mo vs prior 12mo)
  - seasonalityCurve (12-element normalized monthly avg, peak=100)
  - peakMonth / troughMonth
"""
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
import time

ROOT = Path(__file__).resolve().parent.parent
LANDMARKS_FILE = ROOT / "scripts" / "landmarks.json"
OUTPUT_FILE = ROOT / "data" / "landmarks_pageviews.json"

API_BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
PROJECT = "en.wikipedia"
ACCESS = "all-access"
AGENT = "all-agents"
GRANULARITY = "monthly"
USER_AGENT = "platinumlist-expansion-map/1.0 (analysis@platinumlist.ae)"


def fetch_pageviews(article: str, start: str, end: str) -> list[dict]:
    """Return monthly pageviews for article between YYYYMMDD dates."""
    article_enc = urllib.parse.quote(article, safe="")
    url = f"{API_BASE}/{PROJECT}/{ACCESS}/{AGENT}/{article_enc}/{GRANULARITY}/{start}/{end}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get("items", [])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []  # article doesn't exist
        raise
    except urllib.error.URLError as e:
        print(f"  !! network error for {article}: {e}")
        return []


def derive_signals(items: list[dict]) -> dict:
    """Compute annual, YoY, seasonality from monthly items."""
    if not items:
        return {"annualPageviews": 0, "yoyGrowthPct": None, "seasonalityCurve": None}

    # items is chronological; each has 'views' and 'timestamp' like '2023040100'
    monthly = [(item["timestamp"][:6], item["views"]) for item in items]

    last12 = monthly[-12:] if len(monthly) >= 12 else monthly
    prior12 = monthly[-24:-12] if len(monthly) >= 24 else []

    annual = sum(v for _, v in last12)
    prior_annual = sum(v for _, v in prior12) if prior12 else 0
    yoy = ((annual - prior_annual) / prior_annual * 100.0) if prior_annual else None

    # Seasonality: average each calendar month across 3 years, normalize so peak=100
    by_month = {m: [] for m in range(1, 13)}
    for ts, v in monthly:
        mm = int(ts[4:6])
        by_month[mm].append(v)
    avg_by_month = [
        (sum(vs) / len(vs)) if vs else 0
        for vs in [by_month[m] for m in range(1, 13)]
    ]
    peak = max(avg_by_month) if avg_by_month else 0
    curve = [round(v / peak * 100, 1) for v in avg_by_month] if peak else [0] * 12
    peak_month = avg_by_month.index(peak) + 1 if peak else None
    trough_month = avg_by_month.index(min(v for v in avg_by_month if v > 0)) + 1 if any(avg_by_month) else None

    return {
        "annualPageviews": annual,
        "priorYearPageviews": prior_annual,
        "yoyGrowthPct": round(yoy, 1) if yoy is not None else None,
        "seasonalityCurve": curve,
        "peakMonth": peak_month,
        "troughMonth": trough_month,
        "monthsAvailable": len(monthly),
    }


def main() -> int:
    with open(LANDMARKS_FILE) as f:
        countries = json.load(f)

    end_dt = datetime.utcnow().replace(day=1) - timedelta(days=1)  # last complete month
    start_dt = end_dt.replace(day=1) - timedelta(days=365 * 3)
    start = start_dt.strftime("%Y%m01")
    end = end_dt.strftime("%Y%m%d")
    print(f"Window: {start} → {end}")

    result = {}
    for country, articles in countries.items():
        print(f"\n[{country}]")
        country_out = {"landmarks": [], "countryTotals": {}}
        country_annual = 0
        country_prior = 0

        for article in articles:
            items = fetch_pageviews(article, start, end)
            sig = derive_signals(items)
            country_out["landmarks"].append({
                "article": article,
                "displayName": article.replace("_", " "),
                **sig,
            })
            country_annual += sig["annualPageviews"]
            country_prior += sig.get("priorYearPageviews", 0)
            print(f"  {article:40s} {sig['annualPageviews']:>10,}  YoY {sig['yoyGrowthPct']}")
            time.sleep(0.05)  # 20 rps cap, very conservative

        # Country-level rollups
        country_out["landmarks"].sort(key=lambda x: x["annualPageviews"], reverse=True)
        country_out["countryTotals"] = {
            "totalLandmarkPageviewsY1": country_annual,
            "totalLandmarkPageviewsY0": country_prior,
            "landmarkYoYGrowthPct": round(
                (country_annual - country_prior) / country_prior * 100.0, 1
            ) if country_prior else None,
            "topLandmark": country_out["landmarks"][0]["displayName"] if country_out["landmarks"] else None,
            "concentrationRatio": round(
                country_out["landmarks"][0]["annualPageviews"] / country_annual * 100, 1
            ) if country_annual and country_out["landmarks"] else None,
        }
        result[country] = country_out

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"_source": "Wikipedia Pageviews API", "_window": [start, end], "data": result}, f, indent=2)

    print(f"\n✓ wrote {OUTPUT_FILE}")
    print(f"  {len(result)} countries · {sum(len(v['landmarks']) for v in result.values())} landmarks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
