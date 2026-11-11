# Q&A prep sheet (v2)

Questions can go to **any** of us, and everyone should be able to talk about the whole project. Skim this plus [`plain_english_faq.md`](plain_english_faq.md) before Dec 3. The sections follow the question types the professor said she would ask. Full chart-by-chart reasoning is in [`visualization_decisions.md`](visualization_decisions.md).

**Answer pattern that works:** (1) one-sentence answer, (2) the number or chart that backs it, (3) the honest limit. If you do not know, say what the data shows and say "we did not test why."

---

## "Why did you choose these visual representations and encodings?"

- **Q1 pressure:** One line, because the task is "how has this changed over time." Position is the most accurate way to show a number. All disruption windows are the same gray and labeled by name, so the trend leads and there is no color legend to decode.
- **Q2 lanes:** Two lines on a shared axis, the same blue and orange and the same gray bands as Q1 on purpose, so the charts line up and can be compared directly.
- **Q3 ports:** A line chart for ships waiting, plus a proportional-symbol map. On the map, circle area encodes only what the data supports, a throughput slump, not literal wait times, because wait counts exist for only 2 of the 9 ports.
- **Q4 synthesis:** An episode scorecard (a table of bars). Rows are disruptions, columns are measures, so you read across a row and see whether pressure, cargo shift, and ship backlog moved together. The older stacked-strips chart is in the backup slides.

## "How do your visualizations support your analytical tasks?"

- Q1: identify trend and magnitude over about 30 years.
- Q2: compare two groups over time and detect a shift in a window.
- Q3: find extremes (worst backlog) and locate them (map).
- Q4: compare episodes and check whether three measures move together.

## "What conclusions can reasonably be drawn?"

- Cargo does shift between lanes, and the direction depends on the **type** of disruption: a port jam pushed cargo east (the East and Gulf share rose 8.4 points in 2021-22), while canal and Red Sea problems nudged it west.
- 2026 looks like the chokepoint pattern so far: pressure is elevated (peak 1.81, 1.28 in September), cargo is leaning west (down 2.7 points), and port backlogs are near record lows.
- **Not** supported: anything about non-China trade, anything causal from the correlations, a precise ship-waiting ranking across all 9 ports (BTS publishes it for 3 groups), or a forecast from shipping prices.

## "How did you evaluate effectiveness and integrity?" (have two examples ready)

1. **A wrong percentage we caught.** Our notes said September 2026's 1.28 was "about 40% of the 2021 peak." 1.28 divided by 4.43 is about 29 percent. The 40 percent applies to the 2026 peak of 1.81. We fixed the slide and the notes.
2. **An overclaimed statistic.** The pitch called the shipping-price link "the signal that predicts the reroute." The correlation is 0.48, which sounds like confirmation. Splitting it shows 0.82 through 2022 and 0.09 since. We rewrote the claim.
3. **A misattributed cause.** A drop in lane share had been pinned on the Panama drought. The data shows the drought alone left no net change (the share swung between 30.6% and 32.9%, then ended where it started at 31.3%); the drop came later, in the Red Sea window. Fixed in the slide and the README.
4. **An unsupported guess.** An early draft called a 2025 trade spike "likely tariff front-loading." We had no evidence, so the README says "that's a guess, not a finding."
5. **A broken workbook.** A script generated a Tableau file that Tableau refused to open. We documented it as broken and built the workbook by hand from a step-by-step guide.
6. **A recovery claim that was too broad.** "West Coast ports recovered in 2 to 3 months" was true of Los Angeles and Long Beach only. Oakland and Seattle-Tacoma each took 16 months, and Seattle-Tacoma then fell back to 78 by July 2026, the one port clearly below 2019.

## "What alternatives did you consider and reject?"

- **Mexico as a stand-in for canal traffic:** rejected. Mexico is now the #1 source of US imports, but about 90% of that trade is truck and rail, so it cannot show a sea-route choice.
- **A second y axis for shipping price:** rejected, two scales on one plot invite false claims about co-movement.
- **Stacked strips as the main Q4 chart:** moved to backup. Four wiggly lines are hard to compare by eye. The scorecard and a price scatter show it better.
- **A state-shaded choropleth for ports:** rejected, our data belongs to nine points, and shading whole states adds area bias.
- **A color per disruption:** rejected, it would compete with the lane colors and force a legend lookup.
- **Generating the Tableau workbook with a script:** rejected after it failed to open.

## "What limitations remain?"

- Four disruption episodes is a small sample: a pattern, not proof.
- Two episodes (Panama drought and Red Sea) overlap and cannot be fully separated.
- China-origin data only: about 8% of US goods imports in Jan to Sep 2026 (7.8%), down from 13.4% in 2024 (Census).
- Lane share is dollar value, not container counts.
- Ship-waiting counts are published for LA-Long Beach, Savannah, and "all other ports" only.
- Correlations are not significance-tested, and monthly points are not independent.
- Data runs about 2 to 3 months behind.

## "What additional analysis would be valuable?"

- Repeat the lane-share analysis for a second origin country (Vietnam, for example).
- Find a true per-port wait series to replace the throughput-slump proxy on the map.
- Test the labor-dispute and diversion explanations directly instead of citing outside reporting.

---

## Likely audience questions and one-line answers

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
| What is your conclusion? | Not over, but a different crisis. 2021 was a port jam: pressure, freight costs and ships waiting all spiked, and cargo moved east. 2026 is a cost shock: pressure and freight rates up, ports clear, cargo leaning west. A pattern from four episodes, not proof. |
| Why is pressure high in 2026 but ports are clear? | **Our data:** the pressure score peaked at 1.81 in May 2026 and was 1.28 in September, the Shanghai to Los Angeles rate rose from $3.1k (Apr) to $7.8k (Sep), yet Los Angeles and Long Beach averaged under 1 ship waiting. So this is not a port queue. **Theory, from outside reporting, not tested by us:** the Middle East war raised fuel costs and lengthened routes, while tariffs cut China's cargo. The NY Fed did not say what drove the index ([Reuters, Oct 6 2026](https://finance.yahoo.com/economy/policy/articles/york-fed-says-supply-chain-143658302.html)). |
| Do tariffs explain it? | **Partly, as a theory.** Our Census figures show US imports from China fell from $440.3B (2024) to $308.7B (2025) and $215.0B in Jan to Sep 2026, about 8% of US imports, down from 13% in 2024 ([Census, US trade with China](https://www.census.gov/foreign-trade/balance/c5700.html); [Census, top trading partners](https://www.census.gov/foreign-trade/statistics/highlights/topyr.html); PIIE puts it at about 9% by end of 2025, [PIIE, Mar 16 2026](https://www.piie.com/blogs/realtime-economics/2026/trump-china-trade-wars-five-takeaways-us-imports-2025)). Less China cargo fits clear West Coast ports. It does not explain higher pressure, and we did not test cause. |
| What is the war's role? | **Outside reporting, a theory, not our result.** The war began Feb 28 2026 and effectively closed the Strait of Hormuz; bunker fuel roughly doubled and ships went around the Cape ([Sea Vantage timeline](https://www.seavantage.com/blog/strait-of-hormuz-crisis-2026-shipping-disruption-timeline)). Reuters tied April's jump (1.82 first reported; 1.78 in our revised data) to the war's timing but said the NY Fed gave no cause ([Reuters via PYMNTS, May 6 2026](https://www.pymnts.com/supply-chain/2026/fed-data-shows-global-supply-chain-pressure-hits-4-year-high/)). Xeneta reported Far East to US West Coast rates up 192% from Feb 28 to Jun 19 ([Xeneta, Jun 19 2026](https://www.xeneta.com/news/us-iran-deal-to-reopen-strait-of-hormuz-but-full-container-shipping-recovery-at-least-three-months-away)). Note: our pressure score was already 0.47 in Dec 2025, before the war. |
