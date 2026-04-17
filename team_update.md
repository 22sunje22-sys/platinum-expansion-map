# Team update · Expansion map v2.5 — inventory-type demand (Murtaza-inspired)

---

## English

Hey team — shipped an update to the expansion map. Credit where it's due: this was directly inspired by the inventory-type framing Murtaza pushed for on the Spain analysis — "it's not just 'how much demand,' it's 'demand for *what kind* of thing.'" I agreed and generalized it across all 24 markets.

**What's new (Launch tab, every country):**

1. **Inventory-type demand mix** — 12 buckets: museums, attractions, theme parks, water parks, tours, shows, observation decks, religious sites, zoos, historical sites, nature parks, experiences. Each country now shows its demand split across these buckets, derived from GCC search volumes.
2. **Landmark demand proxy** — top 5 SKUs per country with Wikipedia pageviews and YoY (3-year history).
3. **Seasonality curve** — 12-month normalized demand pattern per country (Google Trends, geo=UAE as GCC proxy, 5-year history).

**What this surfaces:**

- Malaysia demand is 50% theme parks · Japan is 49% observation decks — both categories we can't easily contract under current partnership model. Real signal for supply strategy.
- Austria 83% historical sites · Poland 87% · Greece 84% · Portugal 62% — the European historical-sites belt is a single-category thesis, not a diversified one.
- Italy landmarks are −24% to −28% YoY across Colosseum / Pompeii / Pisa — post-2024 peak correction. Doesn't kill Phase 1 thesis but worth flagging.
- Egyptian Museum +323% YoY (Grand Egyptian Museum opening is visibly pulling demand).
- Petra −26%, Cappadocia −18%, Giza −19% — MENAT primaries softening across the board. Supports Jordan/Egypt being Phase 2/Watchlist rather than Phase 1.

**Link:** The map at [platinum-expansion-map.vercel.app](https://platinum-expansion-map.vercel.app/) — click any country, open the **Launch** tab.

**Docs:** Full algorithm notes + data sources in [`docs/data-pipeline.md`](https://github.com/22sunje22-sys/platinum-expansion-map/blob/main/docs/data-pipeline.md). Proposed v2.5 scorecard additions (demand-robustness, category-fit, seasonality-fit) documented but not yet applied to scores — happy to discuss which ones are worth baking in.

**Nothing in the existing scorecard changed** — v2.1 composite scores are intact. This is an additive data layer, not a re-rank.

Integrity-checked across all 7 tabs × 5 representative markets, no regressions.

---

## Русский

Привет команда — выкатил апдейт карты экспансии. Сразу отдам должное — идея пошла от фрейминга Муртазы на анализе Испании: "не просто 'сколько спроса', а 'спрос на *какой тип* инвентаря'". Согласился и обобщил на все 24 рынка.

**Что нового (вкладка Launch, по каждой стране):**

1. **Разбивка спроса по типу инвентаря** — 12 категорий: музеи, аттракционы, тематические парки, аквапарки, туры, шоу, смотровые, религиозные объекты, зоопарки, исторические сайты, природные парки, активности. Для каждой страны теперь видно, на что идёт спрос из GCC.
2. **Спрос по лэндмаркам** — топ-5 объектов в стране с просмотрами Википедии и YoY за 3 года.
3. **Сезонность** — 12-месячная кривая спроса по стране (Google Trends, geo=UAE как прокси GCC, 5-летняя история).

**Что вылезло из данных:**

- Малайзия — 50% спроса на theme parks · Япония — 49% observation decks. Оба — категории, которые мы не контрактуем напрямую в текущей модели. Это сигнал для supply-стратегии.
- Австрия 83% historical sites · Польша 87% · Греция 84% · Португалия 62% — европейский historical-sites пояс это однокатегорийная история, не диверсифицированная.
- Италия: Colosseum / Pompeii / Pisa все −24% до −28% YoY — коррекция после пикового 2024-го. Phase 1 тезис не ломает, но заметим.
- Египетский музей +323% YoY (открытие Grand Egyptian Museum тянет спрос — видно в данных).
- Петра −26%, Каппадокия −18%, Гиза −19% — MENAT primary attractions все проседают. Подтверждает, что Jordan/Egypt это Phase 2/Watchlist, не Phase 1.

**Линк:** карта на [platinum-expansion-map.vercel.app](https://platinum-expansion-map.vercel.app/) — клик на страну → вкладка **Launch**.

**Документация:** полный алгоритм + источники в [`docs/data-pipeline.md`](https://github.com/22sunje22-sys/platinum-expansion-map/blob/main/docs/data-pipeline.md). Новые сабсигналы для v2.5 скоркарда (demand-robustness, category-fit, seasonality-fit) задокументированы, но в скоры ещё не вшиты — готов обсудить, какие из них имеет смысл внедрять.

**В существующем скоркарде ничего не поменялось** — v2.1 композит целый. Это чисто дополнительный слой данных, а не пересчёт.

Прогнал integrity-чек по всем 7 вкладкам × 5 рынкам, регрессий нет.
