#!/usr/bin/env python3
"""
gather_inventory_mix.py — bucket the existing 720-kw DataForSEO pull into
inventory categories (museums / attractions / theme parks / tours / shows /
religious / observation / water-parks / zoos / historical / nature / experiences).

Input: /Users/alexanderyutkin/Desktop/PL_KeywordPlanner_24markets_GCC.csv
Output: data/inventory_mix.json

Note on coverage: existing CSV has 10 kw × destination (4 generic + 6 landmark).
This gives us a *directional* mix, not a full spectrum. For full coverage, a
new DataForSEO pull with inventory_categories.json templates is needed — see
gather_inventory_full.py (not yet built; requires ~300 new API calls).
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_IN = Path("/Users/alexanderyutkin/Desktop/PL_KeywordPlanner_24markets_GCC.csv")
OUTPUT = ROOT / "data" / "inventory_mix.json"

# keyword patterns → bucket. First match wins. Case-insensitive.
BUCKETS = [
    ("theme_parks", re.compile(r"\b(disneyland|universal studios|theme park|amusement|sunway lagoon|europa park|sentosa|tokyo disney)\b", re.I)),
    ("water_parks", re.compile(r"\b(water park|aqua park|wild wadi|atlantis water)\b", re.I)),
    ("museums", re.compile(r"\b(museum|gallery|uffizi|rijksmuseum|van gogh|louvre|british museum|prado|teamlab|miniatur wunderland|egyptian museum|schindler|anne frank|titanic belfast|heineken experience|book of kells|guinness storehouse)\b", re.I)),
    ("religious_sites", re.compile(r"\b(mosque|cathedral|basilica|vatican|sagrada familia|hagia sophia|blue mosque|fushimi inari|kiyomizu|wat |hassan ii|temple)\b", re.I)),
    ("historical_sites", re.compile(r"\b(colosseum|pompeii|acropolis|parthenon|petra|pyramid|valley of the kings|karnak|luxor|abu simbel|pompei|cappadocia|auschwitz|wieliczka|jerash|cesky krumlov|delphi|ephesus|mdina|hypogeum|hagar qim|borobudur|prambanan|ait benhaddou|stonehenge|ayutthaya|hue|my son|cu chi|great wall|terracotta|machu|tulum|chichen|angkor|tower of london|buda castle|wawel|schonbrunn|hofburg|belvedere|chillon|versailles|alhambra|topkapi|pena palace|jeronimos|dubrovnik old town|diocletian palace|citadel|bab|kasbah|hallstatt|matterhorn|edinburgh castle|dublin castle|stirling castle|charles bridge|prague castle|brandenburg gate|reichstag|old town square|hungarian parliament|fisherman|heroes square|alcazar|mezquita)\b", re.I)),
    ("observation_decks", re.compile(r"\b(observation deck|skytree|tokyo tower|shibuya sky|viewpoint|marina bay sands|burj khalifa|eiffel tower|empire state|kl tower|london eye|sky bridge|sky tower|arc de triomphe|petronas|pisa)\b", re.I)),
    ("nature_parks", re.compile(r"\b(national park|nature reserve|botanical|gardens by the bay|keukenhof|plitvice|krka|cliffs of moher|ring of kerry|santorini|mykonos|bali|phi phi|halong|ha long|komodo|wadi rum|dead sea|chefchaouen|hallstatt|jungfraujoch|rhine falls|mount pilatus|mount fuji|pamukkale|sintra)\b", re.I)),
    ("zoos_aquariums", re.compile(r"\b(zoo|aquarium|safari|oceanario|seaworld|ocean park)\b", re.I)),
    ("shows_entertainment", re.compile(r"\b(opera|concert|show|theatre|flamenco|moulin rouge|ballet|musical|phantom|les miserables|balloon ride|hot air balloon|ghibli|broadway)\b", re.I)),
    ("tours", re.compile(r"\b(tour|tours|day trip|excursion|guided|cruise|river cruise|canal cruise|walking tour|hop on|hop off|wine tour|beer tour|food tour|boat trip|safari)\b", re.I)),
    ("attractions", re.compile(r"\b(attractions|things to do|tickets|experience|entry)\b", re.I)),
    ("experiences_activities", re.compile(r"\b(cooking class|wine tasting|spa|hammam|bath|baths|desert safari|hot air|fishing|diving|snorkel)\b", re.I)),
]

# Country name normalization: CSV uses "UK", "Czech" — map to canonical
CSV_TO_CANONICAL = {
    "UK": "United Kingdom",
    "Czech": "Czech Republic",
}


def classify(keyword: str) -> str:
    for bucket, pattern in BUCKETS:
        if pattern.search(keyword):
            return bucket
    return "uncategorized"


def main():
    by_country = defaultdict(lambda: defaultdict(float))
    by_country_total = defaultdict(float)
    samples = defaultdict(lambda: defaultdict(list))

    with open(CSV_IN) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dest = CSV_TO_CANONICAL.get(row["destination"], row["destination"])
            vol = int(row["search_volume_monthly"] or 0)
            if vol <= 0:
                continue
            bucket = classify(row["keyword"])
            by_country[dest][bucket] += vol
            by_country_total[dest] += vol
            if len(samples[dest][bucket]) < 3:
                samples[dest][bucket].append(f"{row['keyword']} ({row['origin']} {vol}/mo)")

    # Normalize → % mix
    result = {}
    for country, buckets in by_country.items():
        total = by_country_total[country]
        if total == 0:
            continue
        mix = {b: round(v / total * 100, 1) for b, v in buckets.items()}
        sorted_mix = dict(sorted(mix.items(), key=lambda x: -x[1]))
        result[country] = {
            "totalMonthlyVolumeGCC": int(total),
            "inventoryMixPct": sorted_mix,
            "dominantBucket": next(iter(sorted_mix)) if sorted_mix else None,
            "topThreeBuckets": list(sorted_mix.keys())[:3],
            "bucketSamples": {b: samples[country].get(b, []) for b in sorted_mix},
        }

    OUTPUT.parent.mkdir(exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump({
            "_source": "Derived from PL_KeywordPlanner_24markets_GCC.csv (DataForSEO, Apr 2026)",
            "_method": "Regex-based keyword classification into 12 inventory buckets, then volume-weighted aggregation per country.",
            "_caveat": "Coverage limited to existing 10 kw × destination. Uncategorized bucket shows how much demand is generic ('country tickets'). For richer coverage, run new DataForSEO pull with inventory_categories.json templates.",
            "data": result,
        }, f, indent=2)

    print(f"✓ wrote {OUTPUT}")
    for c in sorted(result.keys()):
        r = result[c]
        top = ", ".join(f"{b}={r['inventoryMixPct'][b]}%" for b in r["topThreeBuckets"])
        print(f"  {c:18s} {r['totalMonthlyVolumeGCC']:>8,}/mo  {top}")


if __name__ == "__main__":
    main()
