# Platinumlist Global Expansion Map

Interactive D3.js world map for the Platinumlist Global Expansion v4 deck (April 2026). Scope = 24-country shortlist + GCC baseline, ranked on demand / supply / regulatability / economics / GCC affinity / moat.

## Local

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

Static site. Vercel auto-detects — no build step, no framework.

## Files

- `index.html` — the map (self-contained: styles, data, D3 logic)
- `world-geojson.js` — simplified country geometries (sets `window.WORLD_GEOJSON`)
- `docs/` — methodology, scorecard, phase plan, financial model, gaps ledger, glossary, **data pipeline**
- `scripts/` — Python auto-gather pipeline (Wikipedia + pytrends + DataForSEO classifier)
- `data/` — gathered signals (`country-signals.json` consumed by `index.html`)

## Documentation

The map surfaces per-country data + citations. The docs folder surfaces the decision logic behind the map.

| Doc | What it covers |
|---|---|
| [docs/methodology.md](docs/methodology.md) | Seven-lens framework · v3 → v4 reframe · Pass 2 re-rank |
| [docs/scorecard.md](docs/scorecard.md) | v2.1 composite · lens weights · catalyst overlay |
| [docs/turkey-flag-filter.md](docs/turkey-flag-filter.md) | 5 auto-DQ criteria |
| [docs/phase-plan.md](docs/phase-plan.md) | Phase 1/2/3 sequencing + portfolio logic |
| [docs/financial-model.md](docs/financial-model.md) | Y1 GMV envelope · Year-3 ARR framing |
| [docs/pass2-signals.md](docs/pass2-signals.md) | DataForSEO keyword methodology · landmark audit |
| [docs/data-pipeline.md](docs/data-pipeline.md) | v2.5 auto-gathered signals · Wikipedia + pytrends + inventory classifier |
| [docs/operational-playbook.md](docs/operational-playbook.md) | Per-market contracting sequence |
| [docs/data-sources.md](docs/data-sources.md) | TAC · Keyword Planner · CSVs |
| [docs/gaps-ledger.md](docs/gaps-ledger.md) | 10 unresolved questions |
| [docs/glossary.md](docs/glossary.md) | Klook belt · Burj-class · regulatable-open · Khaleeji |

## Data source

Deck v4 · April 2026 · Platinumlist Global Expansion.
