# Tableau Story: speaker notes by person

Each of us presents our own view of the Tableau Story. For every view, cover three things in this order: **the analytical question**, **how the visualization answers it**, and **the design decisions** that make it effective. Then say what it shows. The spoken version fits the time budget. The sections after it (design decisions, numbers, likely questions) are what you need if someone asks a follow-up.

**Story link:** https://public.tableau.com/views/SupplyChainResilience-Team/Story

**Same in every view:** blue is the Pacific route (West Coast ports), orange is the Panama route (East and Gulf ports), gray bands are the four episodes. Titles are in Title Case with a one-line subtitle that says how to read the chart. Raul clicks through the Story. When you finish, name the next speaker.

| Story point | Presenter | Time | Headline in the Story |
|---|---|---|---|
| 1 Pressure | Jason | 54s | 2021 peaked; but there is still pressure. |
| 2 Lanes | Paven | 50s | Congestion moved cargo east. |
| 3 Ports | Supriya | 65s | West Coast ports slumped hardest. |
| 4 Scorecard | Raul | 53s | Port jams push cargo east. Chokepoints push it west. |
| 5 Summary | Raul | 22s | 2026 is a cost shock with clear ports. |

**Design vocabulary to reuse (from the course):** *mark* (line, bar, circle), *channel* (position, length, size, color), *position on a common scale* is the most accurate channel, *length* is next, *size* and *color* are less accurate and good for categories or rough size. *Preattentive* means the eye finds it without searching (a single orange bar among gray ones).

---

## Story 1: Pressure (Jason)

**On screen:** a line chart titled "Global Supply Chain Pressure Index, 2019 to 2026". Subtitle: "Higher means more strain on global shipping. Gray bands mark our four episodes."

**The three things to cover**

- **Analytical question:** How stretched is the supply chain right now, compared with the 2021 crisis and the 2023 to 2024 episodes? The task is to compare the size of pressure over time.
- **How the view answers it:** One value per month (the New York Fed's pressure score, where 0 is an average month). Time runs left to right, height is pressure. Read the line against the dashed line at 1 (clearly stressed) and against the gray bands, which mark the four episodes.
- **Design decisions:** see the list below.

**Say** (about 54s, 135 words):

> "My question: how stretched is the supply chain now, compared with past disruptions? A line chart answers it. Time runs left to right, and height is pressure, the easiest thing for the eye to compare. Zero is a normal month, and the dashed line at one is clearly stressed. Design choices: one dark line, so the trend leads; every episode is the same gray band, labeled by name, so there is no color legend to decode; and the pandemic spike is labeled, so nobody wonders why it is not one of our four. What it shows: pressure peaked at 4.43 in December 2021. The canal drought and the Red Sea barely moved it, about 0.2. In 2026 it peaked at 1.81 in May, about 40 percent of that, and was still 1.28 in September. Paven?"

**Do:** point at the "Dec 2021 peak: 4.43" label, then sweep right to the 2026 line. Say "Paven?" and stop.

**Design decisions, and why (for follow-up questions)**

- **A line for a time series.** A line connects the months, so the eye sees trend, peaks and dips at once. The number is encoded by **position on a common scale**, the most accurate channel.
- **One dark gray line, no color for the measure.** Color is reserved for routes (blue and orange) in the other views, so it keeps one meaning across the whole Story.
- **Episodes as gray bands behind the line, all the same gray and labeled by name.** The viewer does not need a legend to decode them. The bands are drawn on a second axis that holds only the band, behind the line, so the line is never hidden.
- **Reference lines at 0 and at 1.** They give the number a meaning without a lookup. The y-axis is titled "Pressure (0 = normal)".
- **Only two direct labels on the line:** the Dec 2021 peak (4.43) and the pandemic wave, marked "not one of our four episodes". Those are the two things an audience member will ask about. We did not label every point, so the chart stays clean.
- **Descriptive title plus a how-to-read subtitle.** No x-axis title, because the years are self-explanatory.
- **Tooltip names the episode** ("Outside our four episodes" for the other months), so hovering answers "which window is this?".
- **The series starts in Jan 2019** so there is a pre-pandemic baseline, and it matches the start of the other two datasets.

**Numbers to have ready**

- Peak **4.43 in Dec 2021**, the highest in the series. All 24 months of the 2021 to 2022 episode were above 1 (episode average 2.66).
- Pandemic spike: **3.47 in Apr 2020**.
- Canal drought and Red Sea: peak **0.20** (averages -0.53 and -0.25).
- 2026: climbed from 0.47 in Dec 2025, **peak 1.81 in May**, **1.28 in Sep**. Above 1 in 5 of 9 months. 1.81 is about **41%** of 4.43. 1.28 is about **29%** of 4.43. Say "about 40 percent" only about the May peak.
- Past values are revised with each release. Our snapshot was downloaded Oct 15, 2026.

**If asked about this view**

| Question | Answer |
|---|---|
| What is the pressure score? | The New York Fed's monthly gauge of global supply chain strain. It combines 27 measures (global shipping and air freight costs, and delivery times, backlogs and stock levels from manufacturer surveys in seven major economies) into one number, in standard deviations from the long-run average. 0 is average. [NY Fed](https://libertystreeteconomics.newyorkfed.org/2022/01/a-new-barometer-of-global-supply-chain-pressures). |
| Why is 1 "clearly stressed"? | It is our rule of thumb: one standard deviation above average. It is not an official NY Fed threshold. |
| Why is the 2020 spike not an episode? | It was a demand shock at the start of the pandemic. Our question is about freight disruptions at ports and chokepoints, so we study four named episodes. We labeled 2020 so nobody wonders. |
| Why do two bands overlap? | The Panama drought (Jun 2023 to May 2024) and the Red Sea rerouting (Nov 2023 to Dec 2024) overlap for 7 months, Nov 2023 to May 2024. The bands are drawn from the same dates in every view. |
| Is 2026 as bad as 2021? | No. The 2026 peak is about 41% of the 2021 peak. But it stayed above 1 for 5 of 9 months and had not faded by September. |
| Why is pressure high if ports are clear? | Our data cannot say. The score includes shipping costs, and ships waiting at Los Angeles and Long Beach averaged under 1. Outside reporting points to the Middle East war and tariffs. That is a theory we did not test. |

---

## Story 2: Lanes (Paven)

**On screen:** a two-line chart titled "Where China's Imports Landed: West Coast vs. East and Gulf Ports". Subtitle: "Share of the value of US container imports from China, by where they arrive." The legend is titled "Route into the US".

**The three things to cover**

- **Analytical question:** When a disruption hits, does cargo change routes, and in which direction? The task is to compare two groups over time and spot a shift inside a window.
- **How the view answers it:** Two lines on one axis. Blue is the West Coast share (Los Angeles, Long Beach, Oakland, Seattle-Tacoma). Orange is the East and Gulf share (New York-New Jersey, Savannah, Virginia, Charleston, Houston). If orange rises while blue falls inside a gray band, cargo moved east.
- **Design decisions:** see the list below.

**Say** (about 50s, 126 words):

> "My question: when something goes wrong, does cargo change routes, and which way? Two lines answer it: blue is the share of China's container cargo value landing at West Coast ports, orange is the share at East and Gulf ports. Design choices: the same timeline and gray bands as the pressure chart, so your eye drops straight from one to the other; the route colors from the map; and three-month averages, so one noisy month does not look like a trend. What it shows: in the 2021 to 2022 jam, orange rose from 28 to nearly 37 percent, about eight points. Cargo moved east. In the canal drought, orange ended where it started, 31.3 percent, so the drought alone did not move cargo. China only. Supriya?"

**Do:** trace the orange rise inside the first gray band, then the flat orange line through the second band. Say "Supriya?" and stop.

**Design decisions, and why (for follow-up questions)**

- **Same timeline, same bands, same width as the Pressure chart.** Both dashboards are the same size, so on the Summary page the two charts line up and the eye can read straight down one month.
- **Route colors reused from the map and from every other view.** Color already means route, so the audience does not learn a new code.
- **Two lines on one axis, not a dual axis.** Both are shares of the same total, in the same units, so one axis is honest. The axis runs 20 to 75, so changes of a few points are visible. It does not start at zero. That is fine for a line chart where we read change, but say so if asked.
- **Three-month averages.** A single month can swing about 1.5 points on its own, so smoothing keeps one noisy month from looking like a trend.
- **Episode names on the bands**, the same labels as the Pressure chart.
- **Plain-language legend:** "West Coast (Pacific)" and "East and Gulf (Panama)", with a dashboard legend object so the legend stays readable inside the Story.
- **Subtitle defines the measure**, so nobody has to ask "share of what?".

**Numbers to have ready**

- How a window is measured: the average East and Gulf share in the **3 months before** the window versus the **last 3 months** of the window. The difference is in percentage points.
- 2021 to 2022 port jam: **28.3% to 36.7%, +8.4 points**.
- Panama drought: **31.3% to 31.3%, 0.0**. The share swung between 30.6% and 32.9% inside the window and ended where it started.
- Red Sea rerouting: **31.1% to 28.7%, -2.3 points**. 2026 so far: **32.9% to 30.2%, -2.7 points**.
- 2019 average: East and Gulf **28.5%**, West Coast **65.1%**. The remaining about 6% lands at other ports that we do not show, which is why the two lines do not add to 100.
- There is an unexplained spike in early 2025 outside any band. We did not investigate it.

**If asked about this view**

| Question | Answer |
|---|---|
| Why China only? | The choice between the Pacific and the Panama Canal exists mainly for Asian cargo, and China was the largest source of US goods imports through 2022. It is about 8% of US goods imports in Jan to Sep 2026, so our view covers a shrinking slice. We do not claim the pattern holds for other countries. |
| Is this containers or dollars? | Dollars. It is the share of the value of containerized imports from China. The Census port data has values and weights, not container counts. |
| What is a port of unlading? | The port where the ship is unloaded. Census uses it for imports, rather than where the goods clear customs. |
| Did the LA jam cause the shift east? | It is consistent with the data, but we do not claim it is the only cause. The East and Gulf share kept rising after the LA backlog cleared, and outside reporting cites West Coast labor worries. |
| Did the Panama drought move cargo? | Not on its own. The share ended where it started. The 2.3-point drop west comes in the Red Sea window, and the two windows overlap, so we cannot separate them. |
| Why does the axis start at 20? | So both lines fill the chart and a two or three point change is visible. It is a line chart, so we read the change and not the height from zero. |

---

## Story 3: Ports (Supriya)

**On screen:** a map titled "How Hard Each Port Was Hit, and Where It Stands Today" (subtitle: "Loaded containers arriving at each port vs. its own 2019 level. Bigger circles mean a deeper drop.") and, on the right, a line chart with a **Measure** toggle (Loaded Imports Index or Ships Awaiting a Berth).

**The three things to cover**

- **Analytical question:** Which US ports were hit hardest, and where do they stand today? The tasks are to find the extremes and to locate them.
- **How the view answers it:** On the map, each circle is a port. Size shows how far that port's loaded containers fell below its own 2019 level at the low point in 2022 to 2023. Color shows the route. On the right, the same index averaged for each route (100 is the 2019 level), and a toggle to ships waiting for a berth.
- **Design decisions:** see the list below.

**Say** (about 65s, 163 words):

> "My question: which ports were hit hardest, and where do they stand now? Two views answer it. On the left, a map: each circle is a port, and a bigger circle means a bigger drop in loaded containers below that port's own 2019 level. Color is the route. On the right, the same ports as two lines, where 100 is the 2019 level. Four design choices. Each port is compared with itself, so big and small ports share one scale. Los Angeles and Long Beach share one label. Exact numbers sit in the tooltip, so the map stays clean. And a toggle swaps the right chart to ships waiting, without adding a second chart. What it shows: Seattle-Tacoma, Oakland, and Los Angeles-Long Beach fell furthest. The West Coast bottoms out at 78 in March 2023, while East and Gulf stays above 100. On the toggle, Los Angeles-Long Beach peaked at 103 ships in January 2022. Savannah peaked at 39 in August 2022. Raul?"

**Do:** hover over the Seattle-Tacoma circle (low 71, latest 78). Point at the 78 on the right chart. Click **Ships Awaiting a Berth** in the toggle and point at the Los Angeles-Long Beach peak. Leave it on that view and say "Raul?".

**Design decisions, and why (for follow-up questions)**

- **A map, because location matters, but only nine circles.** We did not shade states, because shading adds area bias to nine data points.
- **Circle size has three steps**: no drop, a small drop (under 15 points) and a large drop (15 points or more). Three clear groups are easier to read than small differences between circle sizes. Size is a rough channel, so we use it for rough size.
- **Color is the route**, the same blue and orange as every other view.
- **Each port is compared with itself (2019 = 100).** A big port like Los Angeles and a small one like Charleston share one scale. We use a 3-month average so one odd month does not move the picture.
- **Los Angeles and Long Beach share one label** ("LA / Long Beach"), because they are about 8 km apart and two labels would overlap. Each keeps its own circle and tooltip.
- **Exact numbers live in the tooltip, not on the map.** Putting percentages on the map made it feel cluttered. The tooltip shows the biggest drop in points and the month, the months to recover, and the latest index.
- **One chart with a toggle** swaps between the index and ships waiting. The two measures appear in the same place, so there is no second chart to learn. The title and subtitle change with the toggle.
- **A dashed line at 100** appears only on the index view, because 100 only means something there.
- **Ships waiting uses stand-ins**: Los Angeles-Long Beach for the West and Savannah for the East. The government counts ships waiting only for those two and "all other ports", and "all other ports" mixes every coast, so we leave it out.
- **Two honest notes on the chart:** "2022 to 2023 slump" at the West Coast low, and "Oct 2025: no data reported" for the gap in ships waiting.

**Numbers to have ready**

- How the index is built: loaded import containers (in TEUs) for each port, averaged over 3 months, divided by that port's 2019 monthly average, times 100. The route line is the **simple average** of its ports, so every port counts equally.
- West Coast low: **77.8 in Mar 2023**. East and Gulf stayed above **104.98** from Jul 2022 to Dec 2023, so above its 2019 level.
- Lowest points: Seattle-Tacoma **71**, Oakland **76**, Los Angeles **77**, Long Beach **81**, Virginia **89**, New York-New Jersey **95**, Savannah **99**. Charleston and Houston never dipped below 100.
- Months to recover to 2019: Los Angeles 2, Long Beach 3, Virginia 2, New York-New Jersey 1, Savannah 1, **Oakland 16, Seattle-Tacoma 16**.
- Latest (Jul 2026): Seattle-Tacoma **78** (the one port clearly below 2019), Oakland 99, Los Angeles 126, Long Beach 136, New York-New Jersey 125, Savannah 135, Virginia 123, Charleston 113, Houston **176**.
- Ships waiting (monthly average): Los Angeles-Long Beach peak **103 in Jan 2022**, under 1 in the later windows. Savannah peak **39 in Aug 2022**. All other ports peak 62 in Mar 2022.
- Ships-waiting data starts **Jul 2021** and has **no data for Oct 2025**.

**If asked about this view**

| Question | Answer |
|---|---|
| Does a low index mean congestion? | No. It means fewer containers arrived, and weaker demand is part of that. In our data the slump came in spring 2023, after the waiting had ended. We use the index to show how hard each port was hit, not how long ships waited. |
| Why is Seattle-Tacoma still below 2019? | Our data does not say why. It got back to 2019 in about 16 months, then fell to 78 by July 2026. Outside reporting cites trade friction, Canadian ports and rail routes, and labor and congestion worries. |
| Are the route lines weighted by port size? | No. Each is a simple average of the ports' indexes, so a small port counts as much as a large one. The map and tooltip show each port on its own. |
| Why are there only two lines for ships waiting? | The government publishes ships waiting only for Los Angeles-Long Beach, Savannah and all other ports combined, and only from July 2021. |
| Why does Charleston show a number for July 2026? | Its July report is not out yet, so its latest index averages May and June. |
| Why did you group LA and Long Beach on the map? | They are about 8 km apart, so their labels overlapped. They still have separate circles and tooltips. |
| What does recover mean? | The number of months from a port's lowest point until its index is back at 100, the 2019 level. |

---

## Story 4: Scorecard (Raul)

**On screen:** a table of bars titled "The Four Episodes Compared". Subtitle: "How intense was each disruption, did cargo change routes, and did ships pile up at the port?" Rows are the four episodes in time order. Columns are Peak Supply Chain Pressure, Cargo Shift (points of China import share), and Ships Waiting at LA-Long Beach (average).

**The three things to cover**

- **Analytical question:** Do the four episodes share a pattern? That is, does the type of disruption decide where cargo goes? The task is to compare episodes across three measures.
- **How the view answers it:** Read across a row to see one episode's pressure, cargo shift and ship waiting together. Read down a column to compare episodes on one measure.
- **Design decisions:** see the list below.

**Say** (about 53s, 133 words):

> "My question: do the four episodes share a pattern? One table of bars answers it. Each row is an episode, each column a measure: peak pressure, cargo shift, and ships waiting at Los Angeles-Long Beach. Design choices: bar length, because length is easy to compare; rows in time order; a zero line on the cargo column; and orange for east, blue for west, matching the route colors. What it shows: 2021 has pressure 4.43, cargo east by 8.4 points, and about 41 ships waiting. The canal drought and Red Sea: pressure near 0.2, almost no waiting, cargo flat or west. 2026: pressure 1.81, almost no waiting, cargo west by 2.7 points. A port jam pushes cargo east. A chokepoint problem pushes it west. Two episodes overlap, so this is a pattern, not proof."

**Do:** run a finger across the top row, then down the middle column. Pause on the 2026 row.

**Design decisions, and why (for follow-up questions)**

- **A table of bars: one column per measure.** The three measures have different units (an index, percentage points, ships), so each gets its own axis, and the rows line them up. This beats one chart with three scales.
- **Bar length on a common baseline** for comparing within a column. Length is easy to judge.
- **Rows in time order**: 2021 jam, Panama drought, Red Sea, 2026.
- **Color only on the cargo column**: orange means cargo moved east, blue means west, matching the route colors. The other two columns are neutral dark gray, so direction is the only thing that pops out.
- **A zero line on the cargo column, and a fixed axis from -4 to 9** so the bars are not stretched, and a bar to the right or left is immediately a direction.
- **Exact values printed on the bars** (pressure to 2 decimals, cargo shift with a plus or minus sign, ships to 1 decimal), so nobody has to estimate.
- **Tooltip notes the overlap:** the Panama drought and the Red Sea rows say they overlap another episode.

**Numbers to have ready**

- Peak pressure: **4.43, 0.20, 0.20, 1.81** (2021 jam, Panama drought, Red Sea, 2026).
- Cargo shift (points of East and Gulf share): **+8.4, 0.0, -2.3, -2.7**. Plus means east, minus means west.
- Average ships waiting at Los Angeles-Long Beach: **40.8, 0.7, 0.9, 0.9**. The 2021 figure averages Jul 2021 to Dec 2022 only, because the ships-waiting data starts in July 2021, and the monthly average peaked at 103.
- The Panama drought and the Red Sea windows overlap for 7 months, so their effects cannot be separated.

**If asked about this view**

| Question | Answer |
|---|---|
| Why is the Panama drought's cargo shift 0.0? | The East and Gulf share ended where it started, 31.3%. The drought alone did not move cargo. |
| Why do you say a port jam pushes cargo east? | In 2021 to 2022, with Los Angeles and Long Beach jammed, the East and Gulf share rose 8.4 points, and Savannah's own backlog peaked later. It is a pattern from one big episode, not proof. |
| Why only Los Angeles-Long Beach for ships waiting? | It is the one West Coast group the government reports. Savannah and all other ports are reported too, but Los Angeles-Long Beach is the one tied to the Pacific route. |
| Is four episodes enough? | No. It is a small sample, and two overlap. We call it a pattern, not proof. |
| Does the 2026 row mean the Middle East war caused this? | We did not test the cause. Our data shows pressure up, ports clear and cargo leaning west. Outside reporting ties 2026 to the war and tariffs. |

---

## Story 5: Summary (Raul)

**On screen:** the Pressure and Lanes timelines stacked on the left, and a **Key Takeaways** panel on the right: "2021: Extreme pressure, cargo moved east. 2023 to 2024: Chokepoints, low pressure, cargo moved west. 2026: A cost shock, not a port jam."

**The three things to cover**

- **Analytical question:** Is the crisis over, or is a new one starting? This is the answer to our business question.
- **How the view answers it:** The two timelines are on the same dates, so reading straight down any month shows pressure and cargo route together. 2021: pressure spikes while orange rises. 2026: pressure is up again while orange falls and ports stay clear.
- **Design decisions:** see the list below.

**Say** (about 22s, 54 words):

> "Last, the summary. The pressure and lane timelines are stacked on the same dates, so you can scan down any month. Three takeaways: 2021, extreme pressure and cargo moved east. 2023 to 2024, chokepoints, low pressure, cargo moved west. 2026, a cost shock, not a port jam. Back to the deck for our answer."

**Do:** point at the three takeaways as you read them. Switch back to the deck tab and put up slide 6.

**Design decisions, and why (for follow-up questions)**

- **No new chart type.** The Summary reuses the Pressure and Lanes charts, so there is nothing new to learn at the end.
- **Stacked on a shared time axis**, built to the same width, so a month lines up vertically.
- **Three short takeaways, one for each phase,** instead of a paragraph. The text is the only part with words, so it carries the answer.
- **No legends repeated and no extra annotations**, so the page stays quiet and the takeaways stand out.

---

## Design decisions for the whole Story (anyone may be asked)

**Questions about the Story as a whole**

- **Why a Story, not one dashboard?** A story walks the audience through an argument in order: pressure, lanes, ports, the comparison, the answer. A dashboard is for exploring. Our talk is a guided argument, so we use a story and keep interaction to one toggle and hover tooltips.
- **One finished dashboard per story point.** Each is a fixed 1560 by 660 inside a 1600 by 850 story, so nothing scrolls or overlaps the navigation. Tableau hides a bare sheet's title inside a story, so each sheet sits in a dashboard with its own title and subtitle.
- **The finding is in the headline of each story point,** so the Story reads even with the sound off.
- **Definitions live in the subtitles, not in captions on the Story,** so the pages do not feel cluttered. Longer captions with the data sources stay on the individual sheets in the workbook.
- **One visual system:** the same blue and orange for routes, the same gray bands for episodes, the same title style and fonts, and legends placed as dashboard objects so they do not get cut off.
- **Minimal interaction:** the toggle on the ports view and hover tooltips. The only other interaction is Tableau's automatic highlighting, so nobody needs instructions.
- **The workbook is self-contained.** The data is embedded in the `.twbx`, so it opens without any setup.

