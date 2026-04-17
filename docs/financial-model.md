# Financial model

## Y1 GMV envelope formula

$$ \text{Y1 GMV} = \text{basket} \times \text{conversion} \times \text{traffic} \times \text{launch-coverage-months} \times \text{ramp-factor} $$

- **Basket** — per-country avg cart value (USD). From PL extended-variables CSV.
- **Conversion** — GCC demand share that pre-books × close-rate on contractable supply. Ranges 0.5–2.0% depending on moat + regulatability.
- **Traffic** — Pass 2 DataForSEO full-GCC monthly volume × addressable share.
- **Launch coverage** — months inside Y1 where the market is live (e.g., MY Q3'26 = 6 months Y1).
- **Ramp factor** — conservative discount applied to traffic × conversion for the ramp period. 0.4× (affiliate/execution) · 0.5× (direct anchor).

### Per-market envelopes (Phase 1–2)

| Market | Y1 GMV (USD K) | Conversion | Basket | Launch cadence |
|---|---|---|---|---|
| 🇲🇾 Malaysia | 400–800 | 1.5–2.0% | $32 | Q3'26 · 6mo Y1 coverage · 0.5× ramp |
| 🇸🇬 Singapore | 400–700 | 1.2–1.5% | $36 | Q4'26 · 3mo Y1 coverage · 0.5× ramp |
| 🇮🇹 Italy | 200–500 | 0.5–1.0% | $42 | Q2'26 soft Apr, scale May · 9mo · 0.5× |
| 🇪🇸 Spain | 100–300 | 0.5–1.0% | $38 | Q1'27 · 12mo · 0.4× (ETIAS drag) |
| 🇦🇹 Austria | 100–250 | 1.0–1.5% | $28 | Q1'27 · 12mo · 0.4× |
| 🇯🇴 Jordan | 150–350 | 1.5–2.0% | $55 | Q2'27 · 9mo · 0.5× (API anchor) |
| 🇨🇭 Switzerland | 50–150 | 0.5% | $72 | Q3'27 · 6mo · 0.4× (affiliate) |

## Year-3 ARR framing (directional)

Extrapolated from UK baseline (basket × conversion × traffic) scaled by destination visitors × regulatable-share × contract-close-rate. **Full model not in source CSVs — to be validated post-France 90-day trading data (Q3'26).**

| Phase | Base case | Stretch |
|---|---|---|
| **Phase 1** (MY + SG + IT + ES) | USD 6–10M ARR | USD 14–22M |
| **Phase 2** (AT + JO + CH affiliate) | USD 1.5–2.5M ARR | USD 4–6M |
| **Combined Y3 P1+P2** | USD 7.5–12.5M ARR | USD 18–28M |

- **Y1 combined opex:** USD 1.3–1.7M
- **ROIC base:** 4–7× on Y1 opex
- **ROIC stretch:** 10×+

## Key model assumptions (unvalidated until France Q3'26)

1. UK basket × conversion generalize to France/Italy/Spain with Arabic UX multiplier
2. Contract close-rate ≥60% within 6mo for markets with regulatability score ≥12/20
3. CPC × conversion gives positive unit economics at basket ≥$30 for regulatable markets
4. Phase 1 infrastructure (payments, supply contracts, Arabic CMS) amortizes across Phase 2 — opex stacking, not stacking linearly

See [gaps-ledger.md](gaps-ledger.md) for the full list of unresolved assumptions.
