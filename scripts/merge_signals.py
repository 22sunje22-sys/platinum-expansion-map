#!/usr/bin/env python3
"""
merge_signals.py — combine all new gathered signals into one file.

Inputs:
  data/landmarks_pageviews.json  (Wikipedia)
  data/seasonality.json          (Google Trends via pytrends)
  data/inventory_mix.json        (DataForSEO-derived classification)

Output:
  data/country-signals.json      (canonical per-country schema)

Schema per country:
{
  "landmarks": {
    "top5": [...]            # by Wikipedia annual pageviews
    "totalY1": int,
    "yoyGrowthPct": float,
    "concentrationRatio": float,  # top1 / total (fragility indicator)
    "topLandmark": str
  },
  "seasonality": {
    "peakMonth": int,          # from Google Trends (preferred) OR Wikipedia fallback
    "troughMonth": int,
    "yoyGrowthPct": float,
    "source": "trends" | "wikipedia" | null,
    "curve": [12 floats]       # monthly, peak=100
  },
  "inventoryMix": {
    "totalMonthlyVolumeGCC": int,
    "topThree": [str, str, str],
    "mixPct": {bucket: pct},
    "dominantBucket": str
  },
  "meta": {
    "asOf": "2026-04-17",
    "sources": [...]
  }
}
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def load(name):
    path = DATA / name
    if not path.exists():
        print(f"  ! missing {name} — skipping")
        return None
    with open(path) as f:
        return json.load(f)


def main():
    landmarks = load("landmarks_pageviews.json") or {"data": {}}
    trends = load("seasonality.json") or {"data": {}}
    mix = load("inventory_mix.json") or {"data": {}}
    mix_full = load("inventory_full.json") or {"data": {}}

    # Fallback: for markets missing from existing landmark-based classifier,
    # use the full templated DataForSEO pull. Prefer existing (stronger signal)
    # because it's keyed on actual landmark queries rather than templates.
    # Normalize labels so 'UK' → 'United Kingdom', 'Czech' → 'Czech Republic'.
    LABEL_NORM = {"UK": "United Kingdom", "Czech": "Czech Republic"}
    normalized_full = {}
    for country, entry in mix_full["data"].items():
        canonical = LABEL_NORM.get(country, country)
        normalized_full[canonical] = entry

    for country, entry in normalized_full.items():
        existing_keys = set(mix["data"].keys())
        if country in existing_keys:
            continue
        entry["_source"] = "dataforseo-full-templated"
        mix["data"][country] = entry

    # Union of all country keys
    all_countries = set()
    all_countries.update(landmarks["data"].keys())
    all_countries.update(trends["data"].keys())
    all_countries.update(mix["data"].keys())

    signals = {}
    for country in sorted(all_countries):
        entry = {"meta": {"asOf": date.today().isoformat(), "sources": []}}

        # Landmarks
        lm = landmarks["data"].get(country)
        if lm:
            entry["landmarks"] = {
                "top5": [
                    {
                        "name": l["displayName"],
                        "annualPageviews": l["annualPageviews"],
                        "yoyGrowthPct": l["yoyGrowthPct"],
                        "peakMonth": l.get("peakMonth"),
                    }
                    for l in lm["landmarks"][:5]
                ],
                "totalY1": lm["countryTotals"]["totalLandmarkPageviewsY1"],
                "yoyGrowthPct": lm["countryTotals"]["landmarkYoYGrowthPct"],
                "concentrationRatio": lm["countryTotals"]["concentrationRatio"],
                "topLandmark": lm["countryTotals"]["topLandmark"],
            }
            entry["meta"]["sources"].append("wikipedia")

        # Seasonality: prefer Google Trends, fall back to Wikipedia top-landmark
        t = trends["data"].get(country)
        if t and "seasonalityCurve" in t:
            entry["seasonality"] = {
                "peakMonth": t["peakMonth"],
                "troughMonth": t["troughMonth"],
                "yoyGrowthPct": t["yoyGrowthPct"],
                "source": "trends",
                "curve": t["seasonalityCurve"],
                "query": t.get("query"),
            }
            entry["meta"]["sources"].append("google-trends")
        elif lm and lm["landmarks"]:
            # fallback: use top landmark's seasonality curve
            top = lm["landmarks"][0]
            entry["seasonality"] = {
                "peakMonth": top.get("peakMonth"),
                "troughMonth": top.get("troughMonth"),
                "yoyGrowthPct": top.get("yoyGrowthPct"),
                "source": "wikipedia",
                "curve": top.get("seasonalityCurve"),
                "query": top.get("displayName"),
            }

        # Inventory mix
        m = mix["data"].get(country)
        if m:
            entry["inventoryMix"] = {
                "totalMonthlyVolumeGCC": m["totalMonthlyVolumeGCC"],
                "topThree": m["topThreeBuckets"],
                "mixPct": m["inventoryMixPct"],
                "dominantBucket": m["dominantBucket"],
            }
            entry["meta"]["sources"].append("dataforseo")

        signals[country] = entry

    output = {
        "_schemaVersion": "1.0",
        "_asOf": date.today().isoformat(),
        "_sources": {
            "wikipedia": landmarks.get("_window", "last 3yr"),
            "google-trends": trends.get("_timeframe", "today 5-y") + f" (geo={trends.get('_geo', 'AE')})",
            "dataforseo": "PL_KeywordPlanner_24markets_GCC.csv (Apr 2026)",
        },
        "data": signals,
    }

    out_path = DATA / "country-signals.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✓ wrote {out_path}")
    print(f"  {len(signals)} countries merged")
    for c, e in sorted(signals.items()):
        srcs = "+".join(s[0] for s in e["meta"]["sources"])
        peak = e.get("seasonality", {}).get("peakMonth", "?")
        top_bucket = e.get("inventoryMix", {}).get("dominantBucket", "?")
        print(f"    {c:18s} [{srcs}]  peak={peak}  top={top_bucket}")


if __name__ == "__main__":
    main()
