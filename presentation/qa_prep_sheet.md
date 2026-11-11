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
3. **A misattributed cause.** A drop in lane share had been pinned on the Panama drought. The data shows the drought alone left the share flat; the drop came in the overlapping Red Sea window. Fixed in the slide and the README.
4. **An unsupported guess.** An early draft called a 2025 trade spike "likely tariff front-loading." We had no evidence, so the README says "that's a guess, not a finding."
5. **A broken workbook.** A script generated a Tableau file that Tableau refused to open. We documented it as broken and built the workbook by hand from a step-by-step guide.
6. **A recovery claim that was too broad.** "West Coast ports recovered in 2 to 3 months" was true of Los Angeles and Long Beach only. Oakland took 16 months and Seattle-Tacoma has not recovered.

## "What alternatives did you consider and reject?"

- **Mexico as a stand-in for canal traffic:** rejected, about 90% of that trade is truck and rail.
- **A second y axis for shipping price:** rejected, two scales on one plot invite false claims about co-movement.
- **Stacked strips as the main Q4 chart:** moved to backup. Four wiggly lines are hard to compare by eye. The scorecard and a price scatter show it better.
- **A state-shaded choropleth for ports:** rejected, our data belongs to nine points, and shading whole states adds area bias.
- **A color per disruption:** rejected, it would compete with the lane colors and force a legend lookup.
- **Generating the Tableau workbook with a script:** rejected after it failed to open.

## "What limitations remain?"

- Four disruption episodes only: a pattern, not a law.
- Two episodes (Panama drought and Red Sea) overlap and cannot be fully separated.
- China-origin data only. We have not measured China's share of all US container imports.
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
| Why only China? | The Pacific-versus-canal choice exists for Asian cargo. China is the cleanest case. We do not claim it holds elsewhere. |
| What does the pressure index measure? | The NY Fed's monthly gauge of how stretched global supply chains are, from shipping costs and manufacturer surveys. 0 is average, 1 is clearly stressed. |
| Why does cargo moving between ports matter? | The disruption moves with it. In 2022 the LA jam was followed by Savannah's own backlog. |
| What replaced Mexico? | A direct measure: share of China imports at East and Gulf ports versus West Coast ports, from US Customs port data. |
| Is this about volume? | Lane share is dollar value. Port throughput and ships waiting are volumes and counts. |
| Do ships waiting cause the reroute? | It is consistent with the data. The East and Gulf share also kept rising after the LA backlog cleared, and outside reporting cites West Coast labor worries, so we do not claim waiting ships are the only cause. |
| Why did volume drop at some ports, and how does that tie to wait times? | Waits are high when too much arrives at once. Volume is low when too little arrives. In our data volume dropped below 2019 in spring 2023, after the waiting ended. We did not test why it dropped. |
| Why has Seattle-Tacoma not recovered? | Our data does not say. Outside reporting shows its imports down 18.0% year on year in 2026-Q1 while Vancouver and Prince Rupert grew, with trade friction, Canadian rail routes, and labor and congestion worries cited. |
| What is a congestion versus a chokepoint? | Congestion blocks a destination (a port). A chokepoint blocks a path (the canal, the Red Sea). They push cargo in opposite directions. |
| Do shipping prices predict the shift? | They did through 2022 (r 0.82) and do not since (r 0.09). One episode drove it, so we do not use it to forecast. |
| What is your conclusion? | Not over, not 2021 again. Pressure above normal, ports clear, cargo leaning west. Which route holds up depends on the disruption type. A pattern to watch, not a proven law. |
