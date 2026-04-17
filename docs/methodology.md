# Methodology

## The reframe: global, not European

v3 tunnel-visioned on 10 European markets. The original evaluation covered MENAT, Asia, Europe and GCC outbound equally. v4 opens the aperture to the full 47-country field from the original evaluation, filtered down to **24 actionable markets** across four continents.

- **Europe (16):** UK · France · Italy · Spain · Austria · Switzerland · Germany · Netherlands · Greece · Ireland · Portugal · Czech · Poland · Hungary · Croatia · Malta
- **Asia (7):** Malaysia · Japan · Singapore · Thailand · Indonesia · Hong Kong · South Korea
- **MENAT (5):** Jordan · Egypt · Morocco · Turkey (cautionary tale) · Azerbaijan
- **Long-haul (1):** South Africa

UK (works) and France (launching) are baselines; Turkey is the cautionary tale we built the filter around.

## Seven decision lenses

v4 evaluates every market on seven lenses — three of which are new-in-v4:

1. **GCC demand signal** — TAC flight-search + original Google demand index
2. **Iconic supply** — Burj-class, pre-bookable, brandable (how many players sell the top 5; Jordan/Petra-style state-only counts against)
3. **Ticketing regulatability** *(new in v4)* — state monopoly · direct-only top-3 · state-API presence. Decouples "regulated" from "closed."
4. **Unit economics** — avg ticket, avg basket, CPC, contractable share
5. **Competition** — OTA lockup, Klook belt in Asia
6. **GCC affinity** — visitors, flights, halal infra, Arabic advantage
7. **Turkey-test flags** *(new in v4)* — 5 hard-fail checks, ≥2 = auto-disqualify. See [turkey-flag-filter.md](turkey-flag-filter.md).

New-in-v4: **GCC signal** · **iconic supply audit** · **ticketing regulatability** · **cross-continent scorecard** on one scale · **Turkey-test DQ**.

## v1 → Pass 2 re-rank: what changed

v1 scored on subjective lenses. Pass 2 (March–April 2026) introduced three measurement upgrades that reshuffled the ranking:

### 1. Full-GCC TAM (Pass 2D)

v1 used UAE+KSA as a GCC proxy (~65% of GCC population). Pass 2D added Kuwait · Qatar · Oman · Bahrain (the other ~35%). Small Gulf states contribute **23–53%** additional demand and they skew toward European boutique markets — which reshuffled the ranking.

### 2. Measurable moat (bias ratio)

v1 scored GCC affinity as a subjective /10 judgment. Pass 2 converted it to **GCC bias ratio** = GCC search intent ÷ worldwide search intent.

| Country | Moat (bias ratio) | Moat lens /20 |
|---|---|---|
| Malaysia | 0.21× | 19/20 |
| Singapore | 0.14× | 16/20 |
| Jordan | 0.11× | 16/20 |
| Austria | 0.05× | 12/20 |
| Hungary | 0.05× | 12/20 |
| Switzerland | 0.05× | 12/20 |
| Italy / Spain / France | 0.01× | 3/20 |

High bias ratio = GCC-skewed demand the incumbents don't service natively → moat.

### 3. Live GCC intent validation (Appendix A)

720 keyword-metrics pulled via DataForSEO → Google Ads Keyword Planner (UAE+KSA combined, English, April 2026) cross-checks composite score vs raw GCC search intent. Flags three mismatches:

- **Japan + Singapore underrated** — combined 5.3K/mo from GCC beats IT+ES+MY (4.3K).
- **Austria rank 4 → intent rank 18** — Schönbrunn only 50/mo from UAE. Composite likely overweighted a "Europe premium" proxy.
- **Italy #1 composite → #8 intent** — supply leads but GCC demand is ~half of JP/SG. Italy stays Phase 1 (regulatable-open + supply depth), but Asia corridor deserves sharper look.

### Final v2 ranking

| Rank | Market | Score | Tier |
|---|---|---|---|
| 1 | Malaysia | 85 | Phase 1 Q3'26 (up from #2) |
| 2 | Singapore | 83 | Phase 1 Q4'26 (up from #6) |
| 3 | Japan | 66 | Licensing only (KADOKAWA-style) |
| 4 | Switzerland / Austria | 65 | Phase 2 affiliate / Khaleeji |
| 5 | France / Jordan | 64 | Baseline / Phase 2 state-API |
| — | Italy / Spain | 55 | Phase 1 execution (iconic supply, not discovery) |
