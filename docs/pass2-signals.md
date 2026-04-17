# Pass 2 signals

Pass 2 is the measurable-data upgrade over v1's subjective lens scoring. Two data pulls, one methodology shift.

## Pass 2 · Keyword Planner (Appendix A)

**720 keyword-metrics** pulled via DataForSEO → Google Ads Keyword Planner:
- 24 markets × 10 queries each (4 generic + 6 landmark)
- Geographic scope: **UAE + KSA combined** (initial pull — covers ~65% of GCC population)
- Language: English
- Timeframe: April 2026 monthly volumes

### What it validated

- Japan + Singapore underrated on v1 composite
- Austria rank 4 → intent rank 18 (Schönbrunn only 50/mo UAE queries)
- Italy #1 composite → #8 intent (supply leads, direct GCC demand ~half of JP/SG)

### What it flagged

Three composite-vs-intent mismatches → reshuffled Phase 1 to include Malaysia + Singapore.

## Pass 2D · Full-GCC TAM

v1 used UAE+KSA as GCC proxy. Pass 2D re-pulled the keyword set for all 6 GCC countries (UAE · KSA · KW · QA · OM · BH).

**Finding:** Small Gulf states (KW+QA+OM+BH) contribute **23–53%** additional demand and skew toward European boutique markets. Proxy was systematically underselling the real GCC TAM.

### Why it matters

- Moat ratio (GCC bias) moves materially when the denominator is real-GCC, not UAE+KSA.
- Malaysia's 0.21× moat and Singapore's 0.14× moat both held up under full-GCC — confirming them as Phase 1.
- Jordan jumped from subjective 6/10 to measurable 0.11× moat → Phase 2 eligible.

## Top landmarks per country

Ten landmarks per market scored for:
1. **Pre-bookability** — can it be bought online 24h+ in advance?
2. **Reseller diversity** — more than one OTA lists it?
3. **GCC intent volume** — UAE+KSA monthly search volume on the landmark SKU

**Landmarks passing** (visible in the map's Signals tab) = how many of the 10 top attractions clear all three criteria. 10/10 = full coverage. ≤4/10 = thin supply → usually DQ or Watchlist.

### Examples

| Market | Landmarks passing | Top landmark (GCC vol/mo) |
|---|---|---|
| Malaysia | 10/10 | Sunway Lagoon (280) |
| Singapore | 10/10 | Universal Studios SG (740) |
| France | 10/10 | Disneyland Paris (2,400) |
| Italy | 10/10 | Colosseum (740) |
| Greece | 8/10 | Acropolis (250) — state-gated |
| Malta | 2/10 | Hypogeum (60) — UNESCO cap |
| Poland | 4/10 | Auschwitz (400) — single-SKU dominance |

## Weighted CPC (GCC)

Average Google Ads CPC across the 10 keyword queries per market, weighted by GCC monthly volume. Surfaces the **acquisition cost** reality that basket alone doesn't reveal.

- **Cheapest:** Germany $0.20 · Croatia $0.04 · Czech $0.11
- **Most expensive:** Spain $2.81 · Italy $2.61 · France $2.28

Drives the Economics /20 lens.

## Data provenance

See [data-sources.md](data-sources.md) for the full audit trail — which CSV, which TAC query, which DataForSEO pull.
