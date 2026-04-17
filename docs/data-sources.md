# Data sources & audit trail

Every number in the map and docs traces back to one of four primary sources. **April 2026 cut.**

## 1. Google TAC (flight-search intent)

- **Instance:** Partner dashboard · Flights Reporting Center → Market Explorer → Market Trends
- **Query type:** "Brand + location" + "Not brand" filter
- **Date range:** last 365 days (365d GCC→EU pull baseline)
- **Breakdowns used:** user country code (GCC origins), destination country, destination city
- **Scope:** Total ad opportunities per user-country × destination pair
- **Caveat:** Rounded to nearest 10K/100K/1M depending on volume

Feeds: Demand lens · regional corridor sizing.

## 2. DataForSEO → Google Ads Keyword Planner

- **Query set:** 24 markets × 10 queries each (4 generic + 6 landmark-specific)
- **Total pulls:** 720 keyword-metrics
- **Geographic scope:**
  - **Pass 2 (v1 baseline):** UAE + KSA combined (English)
  - **Pass 2D (v2):** full GCC — UAE + KSA + KW + QA + OM + BH (English)
- **Metrics pulled:** avg monthly search volume · competition index (CI) · CPC low/high
- **Timestamp:** April 2026

Feeds: Demand 30 · Moat 20 (bias ratio) · Economics 20 (weighted CPC) · Supply 20 (landmark intent).

## 3. Platinumlist market-evaluation CSV (internal)

- **Scope:** 47 countries × 40+ variables (v1 original evaluation)
- **Filtered to:** 24-country shortlist (v4 scope)

Feeds: Supply audit · basket · top-ticket · contractable share · onboarding windows · regulatability profile.

## 4. Platinumlist extended-variables CSV (internal)

- **Scope:** 24 extended-shortlist markets × deeper per-country ops data (Sdn Bhd timelines, payment-rail support, Arabic-UX flag, MDEC status, etc.)
- **Timestamp:** April 2026

Feeds: Operational playbook · per-market qualifiers.

## What's NOT in source CSVs

- **Financial model** — Y1 GMV envelopes + Year-3 ARR framing are directional extrapolations from UK baseline. To be validated post-France 90-day trading data (Q3'26).
- **Catalyst overlay** — judgment-based layer on top of the scorecard. Each +10 catalyst stack cites three independent triggers (campaign + air + event), but the *weight* (+10 vs +5) is qualitative.
- **Phase assignments** — driven by scorecard + portfolio logic (summer + shoulder bundling), not a single data column.

## How to reproduce

1. **TAC pulls:** use the `pl-google-travel-analysis` skill (`.claude/skills/pl-google-travel-analysis/SKILL.md`) with the 4 parameters (date · direction · country · breakdown).
2. **DataForSEO:** the raw pull script lives at `/tmp/dfs_full_pull.py` (per-session scratch — re-generate on demand).
3. **CSVs:** internal to PL analytics workspace.

## Citation convention on the map

Every per-country Evidence tab surfaces **source references** with deck section pointers:
- `Deck v4 · §2 Pass 2 DataForSEO` — keyword-scrape data
- `Deck v4 · §3 Regulatability` — state-monopoly / API flags
- `Deck v4 · §4 Scorecard filter` — DQ flag results
- `Deck v4 · §5 Catalyst overlay` — mega-event / air / campaign stack
- `Deck v4 · §6 Y1 GMV envelope` — per-market launch math
- `Deck v4 · §7 Phase plan` — Q'26–Q'27 sequencing
