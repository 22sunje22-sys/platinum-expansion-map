# Scorecard (v2.1)

## Formula

**Composite = Base /100 + Catalyst overlay /10 → /110**

**Base /100 = Demand /30 + Supply /20 + Moat /20 + Economics /20 + Strategic /10**

### Lens weights (v2 · Pass 2)

| Lens | Max | What it measures | Source |
|---|---|---|---|
| Demand | 30 | Full-GCC TAM (UAE+KSA+KW+QA+OM+BH monthly search volume) | DataForSEO / Google Ads Keyword Planner |
| Supply | 20 | 10-landmark audit — how many of the top-5 attractions are pre-bookable and multi-reseller | Manual scrape + OTA coverage check |
| Moat | 20 | GCC bias ratio = GCC intent ÷ worldwide intent. High ratio = defensible GCC-skew | DataForSEO |
| Economics | 20 | Avg ticket · avg basket · weighted CPC · contractable share | Keyword Planner CPC + PL internal data |
| Strategic | 10 | Iconic supply class · air corridor · regulatability profile · phase-fit | Judgment, documented per market |

### Why these weights

- **Demand 30**: GCC search intent is the closest live-data proxy for willingness-to-pay in this vertical. Can't game it.
- **Supply 20**: Thin supply (≤4/10 landmarks passing) caps revenue regardless of demand.
- **Moat 20**: The only lens that's *defensible over time*. High GCC bias = Klook/GYG can't parachute in.
- **Economics 20**: Tests whether the acquisition math actually works — CPC can silently kill basket × conversion economics.
- **Strategic 10**: Deliberately the lowest weight. Prevents judgment from dominating measurable signals.

## Catalyst overlay /10

Layered *on top* of the base score. Rewards near-term directional events that shift the market in the next 12–24 months.

| Band | Score | Triggers |
|---|---|---|
| Mega-event + air + campaign | +10 | Combined stack: state-backed tourism campaign AND new GCC air routes AND mega-event (e.g., Olympics, Ryder Cup, Visit Malaysia 2026) |
| Double trigger | +8 | Any two of the three |
| Macro tailwind | +5 | Single durable shift (e.g., ETIAS visa-waiver, post-Olympics tourism halo) |
| Flat default | +3 | Stable market, no negative or positive catalyst |
| Absent / negative | 0 | Active headwinds (Tiqets home market, iDEAL payment friction, MoTA monopoly) |

### Top catalyst stacks (+10 in v2.1)

- **🇲🇾 Malaysia** — Visit Malaysia 2026 government campaign (2M Arab tourists target) · VFS Global MY–GCC visa partnership · Malaysia Airlines KL–RUH/JED 4×weekly resumption.
- **🇯🇴 Jordan** — Saudia BAH→AMM 5×weekly + RJ expansion · Jordan Pass B2B API commercial launch · JTB halal-family campaign 2026.
- **🇮🇹 Italy** — Milano-Cortina 2026 Winter Olympics halo · Gulf Air BAH→MXP/FCO resumption May'26 · Vatican Jubilee 2025 residual tail.
- **🇪🇸 Spain** — Ryder Cup 2027 @ Camiral · Saudia MAD/BCN frequency bump · Turespaña halal-tourism push 2026.

## DQ filter (pre-scorecard)

Before scoring runs, every market passes through the **Turkey-test** (see [turkey-flag-filter.md](turkey-flag-filter.md)). ≥2 flags = auto-DQ regardless of other lens scores. Turkey (4 flags) and Egypt (3 flags) fail out here.
