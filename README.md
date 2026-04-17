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

## Data source

Deck v4 · April 2026 · Platinumlist Global Expansion. See the companion Notion page for methodology, scorecard weights, and replay playbook.
