# Turkey-test DQ filter

Hard-stop scan applied *before* the scorecard runs. **≥2 flags = auto-disqualify.** Named after Turkey, which carries all four and was the cautionary tale the filter was built around.

## The 5 flags

| # | Flag | Threshold |
|---|---|---|
| F1 | State monopoly on ticketing | Single state platform for top-5 attractions with no reseller API |
| F2 | FX volatility | >25% YoY swing in local currency vs USD |
| F3 | PSP blocked | Payment processors (Stripe/Adyen) can't service local issuers |
| F4 | Pre-book rate <5/10 | Fewer than 5 of top-10 landmarks are pre-bookable online |
| F5 | Incumbent SOV >60% | Single OTA controls majority of online ticket inventory |

## 24-market scan results

| Country | Flags | Outcome |
|---|---|---|
| 🇹🇷 Turkey | 4 | DQ · **cautionary tale** (regulatory + FX 150% + PSP blocked + partial pre-book) |
| 🇪🇬 Egypt | 3 | DQ · wait for EGP stabilization + MoTA API release |
| 🇯🇵 Japan | 2 | Licensing only (partial state + ~35% JPY vol + Klook SOV) |
| 🇳🇱 Netherlands | 2 | DQ · Tiqets home market + iDEAL payment friction |
| 🇮🇹 Italy | 1 | Workable (partial pre-book gap, manageable) |
| 🇬🇷 Greece | 1 | State-gated — Watchlist pending hhticket.gr B2B access |
| 🇲🇦 Morocco | 1 | Workable (French-SEO dependency) |
| 🇯🇴 Jordan | 1 | Workable via Jordan Pass B2B API (API-led entry) |
| 🇵🇱 Poland | 1 | Thin supply (4/10) |
| 🇲🇹 Malta | 0 | Workable — UNESCO cap is structural, not regulatory |
| All others | 0 | Workable |

## Why Jordan (1 flag) differs from Greece (1 flag)

Both carry 1 flag but diverge operationally:
- **Jordan** — state-controlled but digital-native via Jordan Pass B2B API → *regulatable-open*, Phase 2 eligible.
- **Greece** — state platform hhticket.gr has no B2B surface → *regulatable-closed*, Watchlist until state deal lands.

This distinction — **regulated vs closed** — is the core conceptual breakthrough of the v4 regulatability lens.
