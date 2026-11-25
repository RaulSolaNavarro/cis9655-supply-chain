# Q&A prep sheet (v4)

Questions can go to **any** of us, and everyone should be able to answer about the whole project. This sheet has the facts behind every number: key terms, where the data comes from, exactly how each metric is calculated, what the limits are, and why we made each decision. Read it with [`story_speaker_notes.md`](story_speaker_notes.md) (per-view notes and view-specific questions) and [`plain_english_faq.md`](plain_english_faq.md). Chart-by-chart reasoning is in [`visualization_decisions.md`](visualization_decisions.md).

**Answer pattern that works:** (1) one-sentence answer, (2) the number or chart that backs it, (3) the honest limit. If you do not know, say what the data shows and say "we did not test why."

**Contents:** 1 The project in 30 seconds, 2 Key terms, 3 Data sources, 4 How each metric is calculated, 5 The four episodes, 6 Limitations, 7 Decisions we made and what we rejected, 8 The professor's question types, 9 Likely audience questions, 10 Questions about the Tableau Story.

---

## 1. The project in 30 seconds

**Question:** Is the supply-chain crisis over, or is a new one starting? **Method:** we compare four disruption episodes (the 2021 to 2022 West Coast port jam, the 2023 to 2024 Panama Canal drought, the 2023 to 2024 Red Sea rerouting, and the 2026 pressure) on three measures: how stressed the global system was, whether China-origin cargo changed routes, and whether ships piled up at ports. **Answer:** the crisis is not over, but it is a different one. 2021 was a port jam: pressure, ships waiting and freight costs spiked, and cargo moved east. 2026 is a cost shock: pressure is up, ports are clear, and cargo is leaning west. This is a pattern from four episodes, not proof.

---

## 2. Key terms

| Term | Plain meaning | How we use it |
|---|---|---|
| **Pressure score (GSCPI)** | The New York Fed's Global Supply Chain Pressure Index. A monthly number for how stretched global supply chains are. It combines 27 measures: global shipping and air freight costs, plus delivery times, backlogs and stock levels from manufacturer surveys in seven large economies. It is in standard deviations from the long-run average. [NY Fed](https://libertystreeteconomics.newyorkfed.org/2022/01/a-new-barometer-of-global-supply-chain-pressures). | 0 is an average month. We treat 1 (one standard deviation above average) as "clearly stressed." That threshold is our rule of thumb, not an official line. |
| **Standard deviation** | A typical size of a swing around the average. | We say "pressure score" aloud and avoid the term. |
| **Episode (window)** | A period we study as one disruption. | Four of them, defined in section 5. |
| **Congestion** | A destination is jammed, so ships queue at a port. | The 2021 to 2022 West Coast jam. |
| **Chokepoint** | A path is blocked or made longer, such as a canal or a strait. | The Panama drought and the Red Sea rerouting. |
| **Cost shock** | Costs rise without queues at the ports. This is our label, based on our data. | 2026: pressure and freight rates up, ships waiting near zero. |
| **Route (lane)** | The path cargo takes from China to a US port. | Pacific: straight across to West Coast ports. Panama: through the canal to East and Gulf ports, about 1.9 times as far. |
| **West Coast ports (Pacific-direct)** | Los Angeles, Long Beach, Oakland, Seattle-Tacoma. | Blue in every view. |
| **East and Gulf ports (Panama-dependent)** | New York-New Jersey, Savannah, Port of Virginia, Charleston, Houston. | Orange in every view. |
| **Port of unlading** | The port where a ship is unloaded. | Census assigns imports to this port, not to where goods clear customs. |
| **Containerized value** | The dollar value of goods that arrived in containers. | Basis of the route share. Census reports values and weights, not container counts. |
| **Route share** | The percent of China's containerized import value that lands at one group of ports. | Share at West Coast ports and share at East and Gulf ports. About 6% lands at other ports, so the two do not add to 100. |
| **Percentage point** | A difference between two percentages. Going from 28% to 36% is 8 points. | The unit of cargo shift. |
| **Cargo shift** | How much the East and Gulf share changed over an episode, in points. Positive means east, negative means west. | The middle column of the scorecard. |
| **3-month average** | The average of the current month and the two before it. | Smooths noise in the route share and the port index. |
| **TEU** | Twenty-foot equivalent unit, a standard container size. A 40-foot box is 2 TEU. | BTS reports loaded imports in TEUs. |
| **Loaded imports index** | A port's 3-month average of loaded import containers divided by its own 2019 monthly average, times 100. | 100 is the 2019 level. Below 100 means fewer containers than in 2019. |
| **Trough (slump)** | A port's lowest index between Jul 2022 and Dec 2023. | Sets circle size on the map. Slump = 100 minus the trough. |
| **Months to recover** | Months from the trough until the index is back at 100. | 0 for ports that never dipped below 100. |
| **Ships waiting for a berth** | Container ships at anchor waiting for a free berth. BTS publishes it weekly. | Only for Los Angeles-Long Beach, Savannah and all other ports, from Jul 2021. We average the weeks within each month. |
| **Stand-in** | A port that represents a coast in the ships-waiting view. | Los Angeles-Long Beach for the West, Savannah for the East. |
| **BTS** | The Bureau of Transportation Statistics (US Department of Transportation). | Source of port volumes and ships waiting. |
| **Census** | The US Census Bureau's international trade data. | Source of imports by port from China. |

---

## 3. Data sources

| Source | What it gives us | Coverage we use | Quirks and limits |
|---|---|---|---|
| **NY Fed Global Supply Chain Pressure Index** | One global pressure value per month. | Jan 2019 to Sep 2026 (the series starts in 1998). Downloaded Oct 15, 2026. | Past values are revised with each release. No regional breakdown. Measures the global system, not US ports alone. |
| **Census, US imports by port (`porths`)** | Monthly import value by port of unlading, for China (country code 5700), including the containerized value. | Jan 2019 to Aug 2026. | Values and weights only, no container counts. Census sometimes combines ports for confidentiality. We drop the all-ports total row and the low-value pseudo-port. China only. |
| **BTS Supply Chain and Freight Indicators** | Monthly loaded import TEUs for nine ports. Weekly ships waiting for a berth. Shanghai to Los Angeles freight rate (backup slide). | Port volumes Jan 2019 to Jul 2026. Ships waiting Jul 2021 to Sep 2026. | Data arrives about 3 months late. Ships waiting exists only for Los Angeles-Long Beach, Savannah and all other ports. No ships-waiting data for Oct 2025. Charleston's Jul 2026 volume is not reported yet. |

All three are monthly (BTS ships waiting is weekly and rolled up to monthly), start in Jan 2019, and give us one shared timeline. The Tableau data files are in `tableau/data/`.

---

## 4. How each metric is calculated

**Pressure score, window peak and window average.** The value is the NY Fed's number as published. We only mark which months fall inside each episode. The peak is the highest monthly value inside the window. Example: 2021 to 2022 peak = 4.43 in Dec 2021; average = 2.66.

**Route share.** For each month: China's containerized import value at the group's ports, divided by China's containerized import value at all US ports, times 100. West Coast group = Los Angeles, Long Beach, Oakland, Seattle-Tacoma. East and Gulf group = New York-New Jersey, Savannah, Port of Virginia, Charleston, Houston. The chart plots the **3-month average** of each share. Example: the 2019 average was 28.5% East and Gulf, 65.1% West Coast, and about 6% elsewhere.

**Cargo shift (points).** The average monthly East and Gulf share over the **last 3 months** of an episode, minus the average over the **3 months before it began**. Example, the 2021 to 2022 jam: 36.7% minus 28.3% = **+8.4**. Positive means cargo moved east. Negative means west. About zero is "No change."

**Loaded imports index.** For each port and month: the 3-month average of loaded import TEUs, divided by that port's average monthly TEUs in 2019, times 100. Example: Seattle-Tacoma's lowest point was 71 in Mar 2023, so it was carrying 71% of its 2019 volume. The **route line** is the simple average of its ports' indexes, so every port counts equally. Example: West Coast line in Mar 2023 = average of Los Angeles, Long Beach, Oakland and Seattle-Tacoma = 77.8.

**Map circle size.** Slump = 100 minus the port's lowest index between Jul 2022 and Dec 2023. Size has three steps: no drop (0), small drop (under 15 points) and large drop (15 or more). Example: Seattle-Tacoma 100 - 71 = 29 points, a large drop. Charleston's lowest was 107, so no drop. Months to recover = months from the lowest point until the index is back at 100.

**Ships waiting.** BTS counts ships waiting each week. We average the weeks inside each month. The peak is the highest monthly average. Example: Los Angeles-Long Beach peaked at 102.6 in Jan 2022. "Months to clear" = months from the peak until the first month below 25% of the peak (5 for Los Angeles-Long Beach, 11 for all other ports).

**Scorecard columns.** Peak pressure = the window's highest pressure value. Cargo shift = as above. Ships waiting = the average of the monthly Los Angeles-Long Beach values during the window. The 2021 to 2022 figure (40.8) covers Jul 2021 to Dec 2022 only, because ships-waiting data starts in July 2021.

**Shipping price and correlation (backup slide).** The Shanghai to Los Angeles rate six months earlier versus the East and Gulf share. r = 0.48 over Aug 2020 to Aug 2026, but 0.82 through 2022 and 0.09 from 2023 on. We do not use it to predict, and it is not significance-tested.

---

## 5. The four episodes

| Episode | Dates | Peak pressure | Cargo shift (points) | Avg ships waiting, LA-Long Beach | Cargo moved |
|---|---|---|---|---|---|
| West Coast port congestion | Jan 2021 to Dec 2022 | 4.43 (Dec 2021) | +8.4 | 40.8 | East |
| Panama Canal drought | Jun 2023 to May 2024 | 0.20 | 0.0 | 0.7 | No change |
| Red Sea / Suez rerouting | Nov 2023 to Dec 2024 | 0.20 | -2.3 | 0.9 | West |
| Renewed 2026 pressure | Jan 2026 to latest month (Sep pressure, Aug cargo) | 1.81 (May 2026) | -2.7 | 0.9 | West |

The Panama drought and Red Sea windows overlap for 7 months (Nov 2023 to May 2024), so their effects cannot be separated. We chose the windows from the dates the disruptions were reported, and we use the same dates in every view.

---

## 6. Limitations

| Limitation | What it means | What we say |
|---|---|---|
| **Four episodes** | A small sample. One big episode (2021) drives much of the pattern. | "A pattern, not proof." |
| **Overlapping episodes** | Panama drought and Red Sea overlap for 7 months, so we cannot separate their effects. | "The 2.3-point drop west comes in the Red Sea window, but they overlap." |
| **China only** | About 8% of US goods imports in Jan to Sep 2026, down from about 13% in 2024. The pattern may not hold for other countries. | "We do not claim it holds elsewhere. Next step: a second origin country." |
| **Dollar value, not containers** | Route share is based on value, so price changes can move it. | "Share of value, not box counts." |
| **Ships waiting is only for 3 groups** | Los Angeles-Long Beach, Savannah and all other ports, from Jul 2021. We cannot rank all nine ports on waiting. | "We use two stand-ins and drop "all other ports", which mixes every coast." |
| **Fewer imports is not congestion** | The port index measures containers arriving. A drop can reflect weaker demand, not a jam. | "The slump came after the waiting ended. We use it to show who was hit, not how long ships waited." |
| **Unweighted route averages** | The route line averages ports equally, so a small port counts as much as a large one. | "The map and tooltips show each port on its own." |
| **3-month averages** | Smoothing delays turning points by about a month and hides one-month spikes. | "We smooth to avoid reading noise as a trend." |
| **Data lag** | Port data runs about 3 months behind. Each series stops at its latest month: Sep 2026 for pressure, Aug 2026 for route share, Jul 2026 for ports. | "Each series shows its latest month." |
| **Data gaps** | No ships-waiting data for Oct 2025. Charleston has no Jul 2026 report yet, so its latest index averages May and June. | "The chart labels the Oct 2025 gap." |
| **Revisions** | The NY Fed revises past pressure values. Our figures are from the Oct 15, 2026 download. Reuters first reported April 2026 at 1.82. Our revised value is 1.78. | "Our numbers match the Oct 15 download." |
| **Cause is not tested** | We show when things happened together, not why. The war and tariffs are outside reporting, not our result. | "A theory we did not test." |
| **Correlations** | The price link is not significance-tested, and monthly points are not independent. | "We use price to describe the shock, not to predict the shift." |
| **Y-axis does not start at zero on the lane chart** | The axis runs 20 to 75 so changes of a few points show. | "It is a line chart where we read change." |

---

## 7. Decisions we made, and what we rejected

**Analysis decisions**

| Decision | Why |
|---|---|
| Start the timeline in Jan 2019 for all three sources | One shared timeline, with a pre-pandemic baseline. Weekly BTS data is rolled up to months. |
| Use China as the origin | The Pacific-versus-canal choice exists mainly for Asian cargo, and China was the largest source of US goods imports through 2022. |
| Replace Mexico with a direct measure | Mexico is now the number one source, but about 90% of its trade moves by truck and rail, so it cannot show a sea-route choice. We use the share of China imports at East and Gulf ports versus West Coast ports. |
| Measure trade by port of unlading (Census `porths`) | It gives us a real route measure. If port data had been unusable, we would have used country level. |
| Use 2019 as the benchmark for ports | The last full year before the pandemic. Each port is compared with itself, so big and small ports share one scale. |
| Use four named episodes, not the 2020 pandemic spike | Our question is about freight disruptions at ports and chokepoints. 2020 was a demand shock. It is labeled on the chart. |
| Measure cargo shift as the last 3 months minus the 3 months before | Avoids reading one noisy month as the answer. |
| Treat 1 as clearly stressed | One standard deviation above average is a plain rule of thumb. It is not an official threshold. |
| Call 2026 a cost shock, and state the theory separately | Our data shows pressure up, ports clear and cargo west. The war and tariffs are outside reporting, so we label them untested. |

**Design decisions** (details per view are in `story_speaker_notes.md`)

| Decision | Why |
|---|---|
| Tableau Story, not one dashboard | A story walks through an argument in order. Dashboards are for exploring. We keep interaction to one toggle and tooltips. |
| One dashboard per story point, fixed 1560 by 660 in a 1600 by 850 story | Nothing scrolls or hides behind the navigation, and the Pressure and Lanes charts line up on the Summary. |
| Blue for the Pacific route, orange for the Panama route, everywhere | One color code for the whole Story, so nobody relearns it. |
| The four episodes are the same gray, labeled by name | Avoids a color per episode, which would compete with the route colors and force a legend lookup. |
| Line charts for time, a table of bars for the comparison, a map for place | Match the mark to the task: trend, comparison, location. |
| Definitions in subtitles, not captions on the Story | Keeps the Story from feeling cluttered. Longer captions with sources stay on the sheets in the workbook. |
| Exact numbers in tooltips, not on the map | The map stayed cluttered with percentages on it. |
| Three circle sizes on the map | Three clear groups read faster than small size differences. |
| Los Angeles and Long Beach share one map label | They are 8 km apart, and two labels overlapped. |
| A toggle on the ports chart | Reuses the same space for two measures instead of adding a chart. |

**Alternatives we considered and rejected**

- **Mexico as a stand-in for canal traffic:** rejected. About 90% of its trade moves by truck and rail.
- **A second y-axis for shipping price:** rejected. Two scales on one plot invite false claims about co-movement.
- **Stacked strips as the main comparison chart:** moved to the backup slides. Four wiggly lines are hard to compare by eye. The scorecard and the price scatter show it better.
- **A state-shaded choropleth for ports:** rejected. Our data is nine points, and shading whole states adds area bias.
- **A color per episode:** rejected. It would compete with the route colors.
- **A filter action that narrows other charts to one episode:** rejected for the Story. It needs instructions, and a talk does not have time for them.
- **Generating the Tableau workbook with a script:** rejected after it failed to open. The final workbook was built by hand in Tableau.

---

## 8. The professor's question types

These follow the question types the professor said she would ask.

### "Why did you choose these visual representations and encodings?"

- **Q1 pressure:** One line, because the task is "how has this changed over time." Position is the most accurate way to show a number. All disruption windows are the same gray and labeled by name, so the trend leads and there is no color legend to decode.
- **Q2 lanes:** Two lines on a shared axis, the same blue and orange and the same gray bands as Q1 on purpose, so the charts line up and can be compared directly.
- **Q3 ports:** A line chart for ships waiting, plus a proportional-symbol map. On the map, circle area encodes only what the data supports, a throughput slump, not literal wait times, because wait counts exist for only 2 of the 9 ports.
- **Q4 synthesis:** An episode scorecard (a table of bars). Rows are disruptions, columns are measures, so you read across a row and see whether pressure, cargo shift, and ship backlog moved together. The older stacked-strips chart is in the backup slides of the web deck.

### "How do your visualizations support your analytical tasks?"

- Q1: identify trend and magnitude over about 30 years.
- Q2: compare two groups over time and detect a shift in a window.
- Q3: find extremes (worst backlog) and locate them (map).
- Q4: compare episodes and check whether three measures move together.

### "What conclusions can reasonably be drawn?"

- Cargo does shift between lanes, and the direction depends on the **type** of disruption: a port jam pushed cargo east (the East and Gulf share rose 8.4 points in 2021-22), while canal and Red Sea problems nudged it west.
- 2026 looks like the chokepoint pattern so far: pressure is elevated (peak 1.81, 1.28 in September), cargo is leaning west (down 2.7 points), and port backlogs are near record lows.
- **Not** supported: anything about non-China trade, anything causal from the correlations, a precise ship-waiting ranking across all 9 ports (BTS publishes it for 3 groups), or a forecast from shipping prices.

### "How did you evaluate effectiveness and integrity?" (have two examples ready)

1. **A wrong percentage we caught.** Our notes said September 2026's 1.28 was "about 40% of the 2021 peak." 1.28 divided by 4.43 is about 29 percent. The 40 percent applies to the 2026 peak of 1.81. We fixed the slide and the notes.
2. **An overclaimed statistic.** The pitch called the shipping-price link "the signal that predicts the reroute." The correlation is 0.48, which sounds like confirmation. Splitting it shows 0.82 through 2022 and 0.09 since. We rewrote the claim.
3. **A misattributed cause.** A drop in lane share had been pinned on the Panama drought. The data shows the drought alone left no net change (the share swung between 30.6% and 32.9%, then ended where it started at 31.3%); the drop came later, in the Red Sea window. Fixed in the slide and the README.
4. **An unsupported guess.** An early draft called a 2025 trade spike "likely tariff front-loading." We had no evidence, so the README says "that's a guess, not a finding."
5. **A broken workbook.** A script generated a Tableau file that Tableau refused to open. We deleted it and built the final workbook by hand in Tableau, from our own guides.
6. **A recovery claim that was too broad.** "West Coast ports recovered in 2 to 3 months" was true of Los Angeles and Long Beach only. Oakland and Seattle-Tacoma each took 16 months, and Seattle-Tacoma then fell back to 78 by July 2026, the one port clearly below 2019.

### "What additional analysis would be valuable?"

- Repeat the lane-share analysis for a second origin country (Vietnam, for example).
- Find a true per-port wait series to replace the throughput-slump proxy on the map.
- Test the labor-dispute and diversion explanations directly instead of citing outside reporting.

### "What alternatives did you consider and reject?"

See section 7 above.

### "What limitations remain?"

See section 6 above.

---

## 9. Likely audience questions and one-line answers

| Question | Answer |
|---|---|
| Why only China? | The Pacific-versus-canal choice exists for Asian cargo, and China was the largest source of US goods imports through 2022 ($439B, 13% of the total, in 2024). But its share is falling: about 8% of US imports in Jan to Sep 2026, fourth behind Mexico, Canada and Taiwan, so our lens covers a shrinking slice. We do not claim the result holds elsewhere. |
| What does the pressure index measure? | The NY Fed's monthly gauge of how stretched global supply chains are, from shipping costs and manufacturer surveys. 0 is average, 1 is clearly stressed. |
| Why does cargo moving between ports matter? | The disruption moves with it. In 2022 the LA jam was followed by Savannah's own backlog. |
| What replaced Mexico? | A direct measure: share of China imports at East and Gulf ports versus West Coast ports, from US Customs port data. |
| Is this about volume? | Lane share is dollar value. Port throughput and ships waiting are volumes and counts. |
| Do ships waiting cause the reroute? | It is consistent with the data. The East and Gulf share also kept rising after the LA backlog cleared, and outside reporting cites West Coast labor worries, so we do not claim waiting ships are the only cause. |
| Why did volume drop at some ports, and how does that tie to wait times? | Waits are high when too much arrives at once. Volume is low when too little arrives. In our data volume dropped below 2019 in spring 2023, after the waiting ended. We did not test why it dropped. |
| Why is Seattle-Tacoma still below 2019? | It got back to its 2019 level by July 2024 (16 months), then fell to 78 by July 2026. Our data does not say why. Outside reporting shows its imports down 18.0% year on year in 2026-Q1 while Vancouver and Prince Rupert grew, with trade friction, Canadian rail routes, and labor and congestion worries cited. |
| What is a congestion versus a chokepoint? | Congestion blocks a destination (a port). A chokepoint blocks a path (the canal, the Red Sea). They push cargo in opposite directions. |
| Do shipping prices predict the shift? | They did through 2022 (r 0.82) and do not since (r 0.09). One episode drove it, so we do not use it to forecast. |
| Prices are up in 2026 but you say they do not predict the shift. Which is it? | Both, for different jobs. We use price to **describe** the shock, not to **predict** the shift. The Shanghai to Los Angeles rate was high in both episodes ($11,730 in Aug 2021; $7,848 in Sep 2026, up from $3,112 in Apr), but cargo moved in opposite directions: east by 8.4 points in 2021-22, west by 2.7 points in 2026. So the disruption type, not the price level, explains the direction. Also, the pressure score already includes shipping costs (container and dry-bulk freight rates and airfreight prices), so high pressure and high prices are not two independent confirmations. |
| What is your conclusion? | Not over, but a different crisis. 2021 was a port jam: pressure, freight costs and ships waiting all spiked, and cargo moved east. 2026 is a cost shock: pressure and freight rates up, ports clear, cargo leaning west. A pattern from four episodes, not proof. |
| Why is pressure high in 2026 but ports are clear? | **Our data:** the pressure score peaked at 1.81 in May 2026 and was 1.28 in September, the Shanghai to Los Angeles rate rose from $3.1k (Apr) to $7.8k (Sep), yet Los Angeles and Long Beach averaged under 1 ship waiting. So this is not a port queue. **Theory, from outside reporting, not tested by us:** the Middle East war raised fuel costs and lengthened routes, while tariffs cut China's cargo. The NY Fed did not say what drove the index ([Reuters, Oct 6 2026](https://finance.yahoo.com/economy/policy/articles/york-fed-says-supply-chain-143658302.html)). |
| Do tariffs explain it? | **Partly, as a theory.** Our Census figures show US imports from China fell from $440.3B (2024) to $308.7B (2025) and $215.0B in Jan to Sep 2026, about 8% of US imports, down from 13% in 2024 ([Census, US trade with China](https://www.census.gov/foreign-trade/balance/c5700.html); [Census, top trading partners](https://www.census.gov/foreign-trade/statistics/highlights/topyr.html); PIIE puts it at about 9% by end of 2025, [PIIE, Mar 16 2026](https://www.piie.com/blogs/realtime-economics/2026/trump-china-trade-wars-five-takeaways-us-imports-2025)). Less China cargo fits clear West Coast ports. It does not explain higher pressure, and we did not test cause. |
| What is the war's role? | **Outside reporting, a theory, not our result.** The war began Feb 28 2026 and effectively closed the Strait of Hormuz; bunker fuel roughly doubled and ships went around the Cape ([Sea Vantage timeline](https://www.seavantage.com/blog/strait-of-hormuz-crisis-2026-shipping-disruption-timeline)). Reuters tied April's jump (1.82 first reported; 1.78 in our revised data) to the war's timing but said the NY Fed gave no cause ([Reuters via PYMNTS, May 6 2026](https://www.pymnts.com/supply-chain/2026/fed-data-shows-global-supply-chain-pressure-hits-4-year-high/)). Xeneta reported Far East to US West Coast rates up 192% from Feb 28 to Jun 19 ([Xeneta, Jun 19 2026](https://www.xeneta.com/news/us-iran-deal-to-reopen-strait-of-hormuz-but-full-container-shipping-recovery-at-least-three-months-away)). Note: our pressure score was already 0.47 in Dec 2025, before the war. |

---

## 10. Questions about the Tableau Story

Per-view questions (pressure, lanes, ports, scorecard, summary) are in [`story_speaker_notes.md`](story_speaker_notes.md). These are the ones that can go to anyone.

| Question | Answer |
|---|---|
| Why a Story and not one dashboard? | A story walks the audience through an argument: pressure, then lanes, then ports, then the scorecard, then the answer. A dashboard is for exploring. We kept interaction to one toggle and hover tooltips so the story reads without instructions. |
| Why is the 2020 spike not one of your episodes? | It is the pandemic demand shock (3.47 in April 2020). Our question is about freight disruptions at ports and chokepoints, so we study four named episodes. The pressure chart labels 2020 so nobody wonders. |
| What is the loaded imports index, and why is 2019 the benchmark? | Containers arriving at a port, 3-month average, compared with that port's own 2019 average (= 100). 2019 is the last full year before the pandemic. Comparing each port with itself lets small and large ports share one scale. |
| Does a low index mean congestion? | No. It means fewer containers arrived, and weaker demand is part of that. In our data the slump came in spring 2023, after the waiting ended. We use it to show how hard each port was hit, not how long ships waited. |
| Are the West and East lines weighted by port size? | No. Each is a simple average of its ports' indexes, so every port counts equally. The map and its tooltips show each port on its own (today Houston is at 176 and Charleston at 113). |
| Why does the ships-waiting view only have Los Angeles-Long Beach and Savannah? | The Transportation Department publishes ships waiting only for those two and "all other ports" combined, from July 2021. "All other ports" mixes every coast, so we leave it out and call the two stand-ins for West and East. |
| What is the gap in the ships-waiting line? | October 2025: no data reported. The chart labels it. |
| What does "cargo shift" mean on the scorecard? | The change in the East and Gulf share of China's container imports, in points, from the three months before an episode to its last three months. Right is east, left is west. |
| Why is the Panama drought's shift +0.0? | The share ended where it started (31.3%), so the drought alone did not move cargo. The 2.3-point drop west comes in the Red Sea window, and the two overlap. |
| Why is "now" July 2026 on ports but September on pressure? | Port data arrives about three months late, and lane data runs to August. Each series shows its latest month. |
| Where is the workbook? | On Tableau Public (https://public.tableau.com/views/SupplyChainResilience-Team/Story) and in the repo as `tableau/team/Supply Chain Resilience - Team.twbx`, with the data embedded so it opens without any setup. |
| Who built which view? | Jason, pressure. Paven, lanes. Supriya, ports. Raul, the scorecard, the summary and the story. All four of us can explain every view. |

