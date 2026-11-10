# Final Presentation Script — Global Supply Chain Resilience

Target: **5:30–6:00 spoken** inside the 7-minute slot (leaves ~1 min of slack), then 3 min Q&A.
Word counts assume ~150 words/min conversational pace. Practice once with a timer — these are starting points, not a contract.

Speaking totals: Jason ~90s, Paven ~100s, Supriya ~70s, Raul ~70s. Adjust live if someone wants more/less.

---

## Slide 1 — Title
**On screen:** Global Supply Chain Resilience · CIS 9655 · Jason Braverman, Paven Oommen, Supriya Singh, Raul Sola Navarro
**Speaker:** none — Jason starts talking as this is up.
**Time:** ~3s

---

## Slide 2 — The Business Question
**Speaker: Jason** · ~35s / 85 words

**On screen (big, minimal):**
- "Is the supply-chain crisis actually over?"
- Four questions, one team: Pressure (Jason) · Lanes (Paven) · Ports (Supriya) · Synthesis (Raul)

**Say:**
> "Everyone remembers 2021 — ships stuck outside LA, prices through the roof. The Fed's own pressure index says the system is still tenser than normal today, in 2026. So we asked: is a new crisis building, or does this just look like the ones we've already seen? We split that into four pieces: how much pressure there is overall, whether cargo actually shifts to different ports when a route breaks, which ports get hit hardest, and which routes hold up best once you put it all together."

---

## Slide 3 — Data & Approach
**Speaker: Paven** · ~45s / 110 words

**On screen:**
- 3 sources: NY Fed pressure index (1998–2026) · US Customs import records, by port · Transportation-dept. ship-backlog & freight-rate feed (weekly)
- Route map image (`route_map.png`) — Pacific-direct vs. Panama-dependent
- Callout: "We tested Mexico as a stand-in for Panama Canal traffic — dropped it once we found 90% of that trade moves by truck and rail, not ship."

**Say:**
> "We pulled three real datasets: the Fed's pressure index back to 1998, US Customs records of what's imported through which port, and a transportation feed that tracks ships waiting outside ports and shipping rates, updated weekly. To talk about routes, we split ports into two groups — ports you can reach straight across the Pacific, and ports you can only reach through the Panama Canal, which is almost twice the distance. We almost used Mexico as a stand-in for Panama Canal traffic, but caught that 90% of that trade moves by truck and rail, not ship, so we dropped it."

---

## Slide 4 — Q1: Pressure (Jason)
**Image:** `gscpi_disruption_windows.png`
**Speaker: Jason** · ~55s / 140 words

**On screen:**
- "The index is still climbing, not back to normal"
- Key numbers: 2021 peak **4.43** (all-time high) · 2023–24 shocks barely moved it (**0.20**) · 2026 so far: **1.81** peak, **1.28** in Sept — about 40% of the 2021 peak and still elevated

**Say:**
> "This is that pressure index over time. Zero is normal, anything over 1 is clearly stressed. The 2021 port jam was the big one — it hit an all-time high in December 2021, and pressure stayed elevated for almost two years. The 2023 Panama drought and the Red Sea attacks barely moved this chart at all — real problems, but narrow ones, not system-wide. Now look at the right edge: pressure's been climbing again since late 2025, and as of this September it was still at about 40% of the 2021 peak and hasn't come back down. We shaded every disruption the same gray and labeled it by name, so your eye follows the trend first, not a rainbow of colors."

---

## Slide 5 — Q2: Lanes (Paven)
**Image:** `lane_share_disruption_windows.png`
**Speaker: Paven** · ~52s / 130 words

**On screen:**
- "Cargo does shift — but which way depends on the disruption"
- West Coast jam (2021–22): Panama-dependent share **28.3% → 36.7%**
- Panama drought alone: flat (**31.3% → 31.3%**) — the real drop came from the overlapping Red Sea window
- Caveat: China-origin trade only

**Say:**
> "This tracks what share of China's imports come through Panama-Canal-dependent ports versus West-Coast ports, month by month. Watch it rise during the 2021 jam — cargo clearly rerouted east, away from the clogged West Coast, by about 8 points. Now watch 2023–24: it barely moves. The Panama drought by itself changed nothing — the small drop we do see lines up with the Red Sea disruption instead, and since those two overlap, we're careful not to claim more than we can separate. One honest caveat: this is China-origin trade only, so we can't yet say it holds for cargo from anywhere else."

---

## Slide 6 — Q3: Ports (Supriya)
**Images:** `port_backlog.png` + `port_map.png`
**Speaker: Supriya** · ~50s / 125 words

**On screen:**
- "Where the rerouted cargo actually landed"
- LA–Long Beach: **103 ships** waiting, Jan 2022 — more than every other US port combined
- West Coast ports recovered in 2–3 months; Sea-Tac still hasn't (as of July 2026)

**Say:**
> "This is where that rerouted cargo actually landed. At the worst point, January 2022, over a hundred ships sat waiting outside LA and Long Beach at once — more than every other US port combined. Savannah got hit later, once cargo arrived from the reroute. The map tells the same story geographically. Circle size there is how far each port's volume fell below normal at the worst point — not literal wait times, because that number only exists for a couple of ports, and we were careful not to show a number the data can't back up. West Coast ports recovered in two to three months. Sea-Tac, in Seattle, still hasn't, as of this past July."

---

## Slide 7 — Q4: Synthesis (Raul)
**Image:** `synthesis_small_multiples.png`
**Speaker: Raul** · ~54s / 135 words

**On screen:**
- "Congestion and chokepoints favor opposite routes"
- Port congestion → Panama-dependent route held up best
- Chokepoint disruption (canal, Red Sea) → Pacific-direct route held up best
- 2026 so far looks like the chokepoint pattern
- Freight-rate link: strong through 2022 (r = 0.82), weak since (r = 0.09) — not a reliable predictor now

**Say:**
> "Putting all three together: port congestion and chokepoint disruptions are opposite problems. Congestion favors the longer Panama route, because the short route is where the jam is. A canal or chokepoint problem favors the short Pacific route instead. 2026's renewed pressure looks like the second pattern so far. We also tested whether shipping rates predict this shift six months out — they did, strongly, through 2022, but that relationship's been weak ever since, so we're not using it to predict anything going forward. Three panels on one shared timeline, so you can see whether pressure, rates, and routing actually move together — instead of us just telling you they do."

---

## Slide 8 — Conclusions & Limits
**Speaker: Supriya (limits)** ~20s / 50 words, **then Raul (conclusion + close)** ~20s / 50 words

**On screen:**
- Limits: only 4 comparable disruptions · 2 of them overlap · China-origin data only
- Bottom line: not back to 2019 normal; which route wins depends on the disruption type

**Supriya says:**
> "Three honest limits. We only have four comparable disruptions, so this is a pattern worth watching, not a proven law. Two of them overlap, so we can't fully separate their effects. And our trade data covers China only, so we don't yet know if other countries behave the same way."

**Raul says:**
> "So where this leaves us: the system isn't back to 2019 normal, and which route holds up next depends on what kind of disruption shows up. We'd want to check this against a second origin country before trusting it further. Thanks — happy to take questions."

---

## Slide 9 — Thank you / Questions
**On screen:** Thank you. Repo + dashboard links.
**Time:** ~2s, transition straight to Q&A.

---

## Design-decision one-liners (already folded into the script above, listed here for quick reference if a question asks "why this chart type")

- **Q1:** One line, not multiple colors per event — shaded disruption windows in the same gray so the trend reads first.
- **Q2:** Same two colors and the same gray windows as Q1, so the two charts compare without learning new chart grammar.
- **Q3 map:** Circle size only encodes what the data actually supports (a throughput-slump proxy); backlog counts aren't shown for ports where they don't exist, instead of guessing.
- **Q4:** Three stacked panels sharing one time axis (small multiples) instead of three separate charts, so alignment — or the lack of it — is visible at a glance, and the freight rate gets its own strip rather than a second, differently-scaled y-axis.
