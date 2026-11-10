# Q&A prep sheet — everyone should skim this before Dec 1/3

The guidelines say questions can go to **any** team member and everyone should be ready to discuss the **entire** project, not just your own piece. This consolidates what's scattered across the four README files into one page, organized by the exact question types the instructor said she'll ask.

## "Why did you choose these visual representations and encodings?"

- **Q1 (pressure):** A single line, because the question is "how has this changed over time." Disruption windows are shaded the same gray and labeled by name instead of color-coded, so the trend itself stays the visual lead, not a legend of colors.
- **Q2 (lanes):** Two lines, same two colors and the same gray windows as Q1 on purpose, so the two charts compare directly without the audience learning a new chart.
- **Q3 (ports):** A bar/line chart for the hard numbers (ships waiting, throughput), plus a map. On the map, circle size encodes only what the data actually supports — a throughput-slump proxy — not the literal berth-backlog count, because that count only exists for 2 of 9 ports. We chose not to imply precision we didn't have.
- **Q4 (synthesis):** Three panels stacked on one shared time axis (small multiples) rather than one chart with two y-axes, so a different-unit series (freight rate) doesn't visually overstate or understate itself against the others.

## "How do your visualizations support your intended analytical tasks?"

- Q1's task is **identifying trend and magnitude** over nearly 30 years — a line chart is the standard answer to that task.
- Q2's task is **comparing two groups' share over time** — two lines on a shared axis is the direct encoding for that comparison.
- Q3's task is **finding extremes and locating them geographically** — a ranked chart plus a map, so "which port" has both a number and a place.
- Q4's task is **examining whether three different series move together** — stacking them on one axis is built for exactly that read.

## "What conclusions can reasonably be drawn from your data?"

- Cargo really does shift lanes, and which way depends on the *type* of disruption: port congestion pushes it onto the longer Panama-dependent route; a canal/chokepoint problem pushes it back onto the shorter Pacific route.
- The 2026 pressure increase looks more like the chokepoint pattern so far (based on lane share and port backlogs), not a repeat of 2021.
- What you **can't** reasonably conclude: anything about non-China-origin trade (data only covers China), anything causal from the correlation numbers (r = 0.48 overall is real but not causal, and the relationship isn't stable — r = 0.82 pre-2023, r = 0.09 since), or a precise berth-backlog ranking across all 9 ports (BTS only publishes that for 3 of them).

## "How did you evaluate the effectiveness and integrity of your visualizations?" (have 2-3 concrete examples ready — this is the one they'll probe hardest)

- We caught our own unsupported causal claim: an early draft called an unexplained 2025 trade spike "likely tariff front-loading." We had no evidence for that, so the README now says explicitly "that's a guess, not a finding."
- We caught a misattribution in two places (a slide and a README): a lane-share drop had been pinned on the Panama Canal drought specifically, when the actual data shows the drought alone left the share flat — the drop lined up with the overlapping Red Sea window instead. Fixed in both places once found.
- We corrected an overclaimed statistic from our own earlier pitch: the pitch deck said the freight-rate correlation was "the signal that predicts the reroute" (r ≈ 0.45). The real number is r = 0.48, which sounds like confirmation — but splitting it by period shows r = 0.82 through 2022 and only r = 0.09 since, meaning the relationship has basically stopped holding. We rewrote the claim instead of keeping the flattering version.
- On the Tableau side: an automated script generated a workbook file that looked fine by every check we could run, but Tableau Desktop refused to open it (a real, specific schema error, not a vague failure). Rather than hide that or silently drop it, we documented it as confirmed broken and rebuilt by hand.

## "What alternative design choices did you consider and why did you reject them?"

- Considered using Mexico as a stand-in for Panama Canal-routed trade; rejected once we found about 90% of US-Mexico trade moves by truck and rail, not ocean freight, so it would have measured the wrong thing.
- Considered a second y-axis for the freight rate in the Q4 synthesis chart; rejected it for a separate stacked strip, since two differently-scaled axes on one plot are an easy way to accidentally mislead on how much two lines actually move together.
- Considered generating the Tableau workbook with a script for speed; rejected (after confirming it broke) in favor of building it by hand in Tableau Desktop, following a step-by-step guide instead.

## "What limitations or sources of misinterpretation remain?"

- Only four disruption episodes total — a pattern worth testing, not a proven causal result.
- Two of those episodes (Panama drought, Red Sea) overlap in time and can't be fully separated.
- Trade-volume data is China-origin only; unconfirmed for other countries.
- Port-level berth backlog is only published for LA-Long Beach combined, Savannah, and "all other ports" lumped together — not all 9 ports individually.
- Data runs about 2–3 months behind the present.
- Correlations aren't significance-tested; both series are smooth/trending, so monthly points aren't fully independent observations.

## "What additional analysis would be valuable?"

- Re-run the lane-share analysis on a second origin country (e.g., Vietnam or Mexico-as-origin, not Mexico-as-routing-proxy) to see if the congestion-vs-chokepoint pattern holds outside China.
- Get a true per-port berth-backlog series if a better data source becomes available, instead of the throughput-slump proxy on the map.
