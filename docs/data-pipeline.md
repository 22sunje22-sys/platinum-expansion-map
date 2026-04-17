# Data pipeline · v2.5 signals

New per-country signals that weren't in the deck — gathered automatically from free + low-cost sources, merged into `data/country-signals.json`, and surfaced in the map's **Launch** tab.

## The three new signals

| Signal | Source | What it tells us |
|---|---|---|
| **Landmark pageviews** (top 5 SKUs · 3yr history) | Wikipedia Pageviews API — free, no auth | SKU-level demand proxy · YoY per landmark · concentration ratio (top-1 / total = fragility) |
| **Seasonality curve** (12-month normalized, peak=100) | Google Trends via pytrends · geo=AE as GCC proxy | When to launch · catalyst alignment · shoulder/peak portfolio logic |
| **Inventory-type demand mix** (12 buckets: museums / attractions / theme parks / tours / shows / religious / observation / water-parks / zoos / historical / nature / experiences) | DataForSEO keyword classifier (regex-bucketed on existing 720-kw pull) | Does our contractable supply match demand mix? Top-demand category per market |

## Why these sources, not TAC

TAC city-view pulls take 2–4 weeks per market (Gaps Ledger #3). Wikipedia + pytrends + existing DataForSEO CSV give us the same directional picture in minutes. TAC is kept for what it uniquely does fast — the GCC×destination corridor matrix in one query.

## Pipeline

```
scripts/
  landmarks.json            ← manual (top 5 SKUs per country, Wikipedia slugs)
  inventory_categories.json ← manual (12-bucket taxonomy, regex patterns)
  gather_landmarks.py       → data/landmarks_pageviews.json
  gather_seasonality.py     → data/seasonality.json  (pytrends)
  retry_seasonality.py      → re-runs failures with longer delays + fallback queries
  gather_inventory_mix.py   → data/inventory_mix.json  (classifies PL_KeywordPlanner_24markets_GCC.csv)
  merge_signals.py          → data/country-signals.json  ← consumed by index.html
```

Run order:

```bash
python3 scripts/gather_landmarks.py      # free · ~2 min
python3 scripts/gather_seasonality.py    # free · ~3 min · may 429, retry runs cleanup
python3 scripts/retry_seasonality.py     # retries failures with backoff
python3 scripts/gather_inventory_mix.py  # instant · regex on existing CSV
python3 scripts/merge_signals.py         # instant · writes country-signals.json
```

## Results summary (April 2026 cut)

**Demand concentration (fragility indicator, top-1 / total landmark pageviews):**

| Country | Top SKU | Concentration |
|---|---|---|
| Poland | Auschwitz concentration camp | ~60% ← single-anchor risk |
| Spain | Sagrada Família | high |
| Italy | Colosseum | 41% |
| Japan | Tokyo Skytree | moderate |
| Austria | Schönbrunn Palace | moderate |

**Landmark YoY — April 2026 signals to watch:**

- **Egyptian Museum +323%** (Grand Egyptian Museum opening effect)
- **Jerash +27%**, **Citadel of Amman +364%** (Jordan secondary-SKU growth even as Petra softens)
- **Sunway Lagoon +37%**, **Singapore Zoo +44.7%**, **Gardens by the Bay +32.7%** (Asian secondaries accelerating)
- **Petra −26%**, **Cappadocia −18%**, **Pamukkale −17%**, **Giza −19%** (MENAT primaries softening — visa friction / geopolitics visible)
- **Italy −24% to −28%** across Colosseum / Pompeii / Pisa (post-2024 peak correction)

**Inventory mix dominants (what each market actually demands):**

| Country | Dominant bucket | % of total |
|---|---|---|
| Austria | historical_sites | 83% |
| Poland | historical_sites | 87% |
| Greece | historical_sites | 84% |
| Malaysia | theme_parks | 50% |
| Japan | observation_decks | 49% |
| Netherlands | museums | 52% |
| Spain | religious_sites | 38% |
| Switzerland | nature_parks | 67% |
| France | museums | 34% |
| UK | observation_decks | 33% |

## How this changes the algorithm (v2.5 proposed)

The existing v2.1 scorecard (/110) has no SKU-level or mix signals. The new data unlocks three sub-signals:

### Sub-signal 1 · Demand-robustness (Supply 20 refinement)

**Rule:** penalty for single-anchor markets. If `concentrationRatio > 55%`, subtract 3 from Supply lens.

Rationale: if the top landmark represents >55% of demand, losing that one contract (or pricing pressure on it) collapses the market thesis. Poland (Auschwitz ~60%) is the canonical example. Spain Sagrada-dominance is similar but offset by Madrid's art-triangle breadth.

### Sub-signal 2 · Category-fit (Supply 20 refinement)

**Rule:** penalty if dominant inventory bucket is uncontractable by PL's current partnership model.

Uncontractable by current model: `theme_parks` (Disney/Universal carrier-level only), `observation_decks` in Asia (direct-lock). Contractable: `museums`, `historical_sites`, `religious_sites`, `tours`, `shows_entertainment`.

Malaysia (50% theme_parks) and Japan (49% observation_decks) both get a −2 on Supply here — the demand mix points at inventory categories we can't easily sign. That's a real signal, not a nice-to-have.

### Sub-signal 3 · Seasonality-fit (Catalyst overlay refinement)

**Rule:** +1 to catalyst if peak month aligns with our contracting window (i.e., we can onboard before peak).

Austria peak = September → onboarding window Feb-Aug fits Austria Q3'26 plan. Jordan peak = December → Q2'27 plan misses fiscal alignment. These shouldn't change the phase; they validate it.

### Scorecard impact (rough simulation)

| Market | v2.1 | v2.5 (new penalties) | Delta |
|---|---|---|---|
| Italy | 108 | 108 | 0 (balanced mix) |
| Spain | 99 | 97 | -2 (single-anchor) |
| Malaysia | 94 | 92 | -2 (theme-park-heavy) |
| Poland | 66 | 60 | -6 (single-anchor + watchlist anyway) |
| Japan | — | — | unchanged (already licensing-only) |

**Nothing changes Phase 1 tiering.** This is an integrity check, not a re-rank. The signals now live in the map's Launch tab so stakeholders can see the raw data behind the scorecard claim.

## Caveats

- **pytrends uses geo=AE as GCC proxy** — UAE has largest GCC online population; KSA would differ especially on halal-seasonal markets. For v3 we should loop all 6 GCC codes individually and average.
- **Inventory mix is directional, not complete.** Only 10 kw × country in the existing DataForSEO pull. A new targeted pull with the 12-bucket templates (scripts/inventory_categories.json) would give us 12 × 10 × 6 GCC = 720 new calls per re-run.
- **Wikipedia pageviews is a proxy for search curiosity, not purchase intent.** Correlates with inbound tourism but isn't the thing itself. Cross-check with DataForSEO volume for high-stakes claims.

## Refresh cadence

Quarterly for pageviews + seasonality (new season signals + post-catalyst confirmation). Annually for inventory mix (new keyword pulls). All scripts are idempotent — re-run writes new timestamp and replaces JSON.
