#!/usr/bin/env python3
"""
gather_inventory_full.py — DataForSEO pull for full inventory-category coverage.

For each of 24 markets × 12 inventory buckets × 3-4 templates = ~1000 queries,
pulled against GCC origins (UAE + KSA as primary; full 6-GCC as Pass 2D has
already shown ~+25% uplift in small gulf states).

Reads AUTH from env var DATAFORSEO_AUTH (base64 login:password).
Falls back to reading /tmp/dfs_full_pull.py if present (dev convenience).

Output: data/inventory_full.json — per-country per-bucket volume + samples.

Note: This is the authoritative version of inventory mix (currently derived
from 10-kw regex-classification in gather_inventory_mix.py). Expensive
(~$3-5 in API credits); run once per quarter.
"""
import json
import os
import re
import time
import requests
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
BUCKETS_FILE = ROOT / "scripts" / "inventory_categories.json"
OUTPUT = ROOT / "data" / "inventory_full.json"

URL = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"

# Location codes from the existing PL DataForSEO script
LOCATIONS = {
    "UAE": 2784,
    "KSA": 2682,
}

# Destinations (country, primary_city_for_city_templates)
DESTINATIONS = [
    ("Italy", "rome"),
    ("Spain", "barcelona"),
    ("Greece", "athens"),
    ("Portugal", "lisbon"),
    ("Austria", "vienna"),
    ("Germany", "berlin"),
    ("Netherlands", "amsterdam"),
    ("Ireland", "dublin"),
    ("France", "paris"),
    ("UK", "london"),
    ("Switzerland", "zurich"),
    ("Czech Republic", "prague"),
    ("Poland", "krakow"),
    ("Hungary", "budapest"),
    ("Turkey", "istanbul"),
    ("Egypt", "cairo"),
    ("Jordan", "amman"),
    ("Morocco", "marrakech"),
    ("Malaysia", "kuala lumpur"),
    ("Singapore", "singapore"),
    ("Japan", "tokyo"),
    ("Thailand", "bangkok"),
    ("Indonesia", "bali"),
    ("Vietnam", "hanoi"),
]


def get_auth():
    env = os.environ.get("DATAFORSEO_AUTH")
    if env:
        return env
    # dev fallback: extract from existing script
    fallback = Path("/tmp/dfs_full_pull.py")
    if fallback.exists():
        for line in fallback.read_text().splitlines():
            m = re.match(r'AUTH\s*=\s*"([^"]+)"', line)
            if m:
                return m.group(1)
    raise SystemExit("Set DATAFORSEO_AUTH env var (base64 login:password)")


def expand_template(template: str, country: str, city: str) -> str:
    # {country} -> "italy", {city} -> "rome", {landmark} dropped (n/a at bucket level)
    return (template
            .replace("{country}", country.lower())
            .replace("{city}", city.lower())
            .replace("{landmark}", ""))


def build_queries():
    with open(BUCKETS_FILE) as f:
        buckets_cfg = json.load(f)
    buckets = buckets_cfg["_buckets"]

    queries = []
    for country, city in DESTINATIONS:
        for bucket_name, cfg in buckets.items():
            for template in cfg.get("templates", []):
                if "{landmark}" in template:
                    continue  # need per-country landmark tables; skip at bucket level
                kw = expand_template(template, country, city).strip()
                if kw:
                    queries.append((country, bucket_name, kw))
    return queries


def batch(iterable, size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def call_api(auth, location_code, keywords):
    post = [{"location_code": location_code, "language_code": "en", "keywords": keywords}]
    r = requests.post(URL, headers={"Authorization": f"Basic {auth}"}, json=post, timeout=60)
    r.raise_for_status()
    data = r.json()
    items = []
    for task in data.get("tasks", []):
        for res in task.get("result", []) or []:
            items.append(res)
    return items


def main():
    auth = get_auth()
    queries = build_queries()
    print(f"Total queries: {len(queries)} · across {len(LOCATIONS)} GCC origins = {len(queries) * len(LOCATIONS)} calls")

    # Group by country+bucket so we can batch within each destination
    by_kw = {}  # (country, bucket, kw) -> {origin: volume}

    for origin_name, origin_code in LOCATIONS.items():
        print(f"\n== Origin: {origin_name} ({origin_code}) ==")
        # DataForSEO accepts up to ~700 keywords per call but we'll batch 100 for safety
        keywords_unique = list({q[2] for q in queries})
        total_batches = (len(keywords_unique) + 99) // 100
        for i, kw_batch in enumerate(batch(keywords_unique, 100)):
            print(f"  batch {i+1}/{total_batches} · {len(kw_batch)} kw ...", end=" ", flush=True)
            try:
                items = call_api(auth, origin_code, kw_batch)
                for item in items:
                    kw = item.get("keyword")
                    vol = item.get("search_volume") or 0
                    cpc = item.get("cpc") or 0
                    for (c, b, k) in queries:
                        if k == kw:
                            by_kw.setdefault((c, b, kw), {})[origin_name] = {"vol": vol, "cpc": cpc}
                            break
                print(f"ok ({len(items)} returned)")
            except Exception as e:
                print(f"FAIL: {e}")
            time.sleep(0.5)

    # Aggregate per (country, bucket)
    agg = defaultdict(lambda: defaultdict(lambda: {"totalVol": 0, "samples": []}))
    for (country, bucket, kw), origins in by_kw.items():
        total_vol = sum(v["vol"] for v in origins.values())
        agg[country][bucket]["totalVol"] += total_vol
        if total_vol > 0 and len(agg[country][bucket]["samples"]) < 5:
            agg[country][bucket]["samples"].append(f"{kw} ({total_vol}/mo)")

    # Normalize to mix
    result = {}
    for country, buckets in agg.items():
        total = sum(b["totalVol"] for b in buckets.values())
        if total == 0:
            continue
        mix = {b: round(data["totalVol"] / total * 100, 1) for b, data in buckets.items() if data["totalVol"] > 0}
        mix_sorted = dict(sorted(mix.items(), key=lambda x: -x[1]))
        result[country] = {
            "totalMonthlyVolumeGCC": int(total),
            "inventoryMixPct": mix_sorted,
            "dominantBucket": next(iter(mix_sorted)) if mix_sorted else None,
            "topThreeBuckets": list(mix_sorted.keys())[:3],
            "bucketSamples": {b: buckets[b]["samples"] for b in mix_sorted},
        }

    OUTPUT.parent.mkdir(exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump({
            "_source": "DataForSEO · inventory_categories.json templates · UAE + KSA",
            "_method": f"{len(queries)} templated queries × 2 GCC origins · live search_volume endpoint",
            "_asOf": __import__("datetime").date.today().isoformat(),
            "data": result,
        }, f, indent=2)

    print(f"\n✓ wrote {OUTPUT}")
    for c in sorted(result.keys()):
        r = result[c]
        top = ", ".join(f"{b}={r['inventoryMixPct'][b]}%" for b in r["topThreeBuckets"])
        print(f"  {c:20s} {r['totalMonthlyVolumeGCC']:>8,}/mo  {top}")


if __name__ == "__main__":
    main()
