# Visualization decisions

This is the "why did you draw it that way" file. Every chart in the project is walked through the vocabulary from CIS 9655 (the syllabus readings and the Geovisualization lecture). Use it two ways: as the source for the "How to read it" and "Why this chart" lines on the slides, and as prep for the professor's Q&A questions about encodings, tasks, integrity, and alternatives.

Course ideas used (short glossary):

- **Data abstraction and task abstraction (Munzner).** Before choosing a chart, say what the data is (a table of months, a table of ports with coordinates) and what the viewer needs to do (find a trend, compare two groups, spot an extreme, locate something).
- **Marks and channels (Munzner).** A mark is the shape drawn (point, line, bar, area). A channel is how a data value controls it (position, length, size, color hue, color lightness). Position and length are the most accurate channels for numbers. Area, color, and shape are less accurate, so they carry secondary information.
- **Expressiveness and effectiveness (Munzner).** Expressive means the picture shows all the data and nothing more. Effective means the most important facts use the most accurate channels.
- **Graphical integrity (Tufte).** Scale and baselines are honest, no distortion of proportions, labels on the chart, no decoration that adds no information. Small multiples (the same chart repeated across a variable) beat clutter.
- **Cairo's qualities.** A good visualization is truthful, functional, beautiful, insightful, and enlightening.
- **Narrative structure (Riche et al.).** A story needs a flow: set up the question, build with evidence, reveal the finding, state what it means. A deck is a guided path, a dashboard is an open one.
- **Geovisualization rules (lecture).** Flow maps use direction, line width, and geographic position as channels. Proportional symbols map a value to symbol area. Choropleth maps have area bias, aggregation (ecological fallacy), the counts-versus-ratios trap, and classification choices. Patterns that hold across several classifications are more trustworthy.

> Note: this file draws on the syllabus and the Geovisualization deck. If the other lecture decks (e.g. perception, color, dashboards, storytelling) add terms the professor emphasizes, add them here and to the slide notes.

---

## Project-level decisions

**Same visual language across all four charts.** One blue for Pacific-direct, one orange for Panama-dependent, one gray for everything else, and the same gray shaded bands for disruption windows. Why: a viewer learns the legend once, so Q1 to Q4 can be compared without relearning. Channel used: color hue, only for the group variable (lane), never decoratively.

**Disruption windows are shaded gray, not color-coded.** Four windows in four colors would compete with the lane colors and force a legend lookup. Gray bands with a text label let the data lines lead (Tufte: data-ink first), and the label names the episode directly (direct labeling instead of a legend).

**One set of definitions shared by every chart.** All four charts import the same `WINDOWS` definition and the same loaders, so every chart uses the same months and the same numbers. This is an integrity decision: no chart can quietly use different dates.

**Counts and ratios are kept apart.** Lane share is a ratio (percent of China's containerized import value). Ship backlog is a count. Throughput is an index (each port against its own 2019 = 100). We do not mix them on one axis. This matches the counts-versus-ratios warning from the geovisualization lecture.

**We say what the data cannot show, on the chart.** The Q3 map is a throughput proxy, not a wait-time count. The Q2 chart is labeled China-origin only. Honest labeling is part of integrity.

---

## Q1: Pressure index (Jason)

| Item | Decision |
|---|---|
| Data abstraction | Table of months (1998 to 2026), one quantitative value per month (standard deviations from average). |
| Task abstraction | Identify trend and magnitude over time; compare the size and duration of four episodes. |
| Chart | Line chart. |
| Marks and channels | Mark: line. Channels: horizontal position = time, vertical position = value. Position is the most accurate channel for both. |
| Why not something else | A bar chart would bury the trend. An area chart implies a "total" that is not meant. Color per episode would add a legend lookup. |
| Baseline | A reference line at 0 (average) and at 1 (clearly stressed) so "how high is high" is visible, not implied. |
| Integrity checks | The y axis starts at a meaningful value (the average), not truncated to flatter a story. The 2021 spike is allowed to dominate: that is the data. |
| Direct labels | Each window is named on the chart. |
| Narrative role | Set the stage: pressure is not back to normal. |

## Q2: Lane share (Paven)

| Item | Decision |
|---|---|
| Data abstraction | Table of months, two quantitative values that sum with "Other" to 100% (share of China containerized import value by lane group), 3-month average. |
| Task abstraction | Compare two groups over time; detect a shift during a window. |
| Chart | Two lines on a shared axis, shared time axis with Q1. |
| Marks and channels | Mark: line. Channels: position for value and time, color hue for lane group (blue or orange). |
| Why a 3-month average | Monthly values are noisy because shipments arrive in lumps. The smoothing is stated on the chart. |
| Why share, not dollars | Share is a ratio, so it shows movement between lanes even when total trade rises or falls. |
| Why two lines, not stacked areas | In a stacked chart only the bottom series sits on a common baseline, so the upper one is hard to read (a Munzner effectiveness point). |
| Integrity checks | y axis range is stated; the caption says China-origin only. The text avoids blaming the canal drought for a drop that lines up with the Red Sea window. |

## Q3: Ports (Supriya)

| Item | Decision |
|---|---|
| Data abstraction | Two tables: weekly ship-backlog counts for LA-Long Beach, Savannah, and All Other Ports; monthly port throughput index for nine ports; plus a table of port coordinates. |
| Task abstraction | Find extremes (which port had the worst backlog), compare recovery speed, and locate the ports geographically. |
| Backlog chart | Lines (time series), colored by lane group, direct-labeled at the ends. |
| Map | **Proportional symbol map.** Mark: circle at each port's location. Channels: geographic position (latitude, longitude), circle area = size of the 2022-23 slump, color = lane group, open ring = never fell below 2019. |
| Why proportional, not graduated | The slump is a continuous measure, and area scales smoothly. Graduated symbols would hide differences between ports. |
| Why a map at all | The question "which ports" has a place answer. The map shows the West Coast slump and the East and Gulf resilience as a geographic pattern in one glance. |
| Why not a choropleth | A choropleth shades areas (states). Our data belongs to nine points, not to states. Shading whole states would add area bias (a big empty state looks more important than a small busy port) and mislead. |
| Integrity checks | The map shows a throughput-slump proxy, not wait times, because ship-waiting counts exist for only 2 of the 9 ports. We label it so. LA and Long Beach circles overlap (they are about 8 km apart); the labels and tooltip separate them. |
| Narrative role | Reveal where the rerouted cargo landed. |

## Q4: Synthesis (Raul)

| Item | Decision |
|---|---|
| Data abstraction | A table of four episodes with three summary measures each (pressure peak, cargo shift in points, average LA-Long Beach backlog), plus the monthly series behind them. |
| Task abstraction | Compare episodes; see whether three different measures rise and fall together; check whether freight rates predict the shift. |
| Route map | Flow-style schematic. Channels: geographic position (the path), line type or color (lane group). It is labeled a schematic because routes are great-circle legs between a few waypoints, not real shipping lanes. |
| **Episode scorecard (main)** | A table of bars. Rows = episodes, columns = measures, bar length = value. Why: aligned bars on a common baseline use length, the second most accurate channel, and the eye reads across a row. It answers "do they move together?" directly. |
| Stacked strips (backup) | Four strips on one time axis: the small-multiples idea (Tufte). We kept the freight rate in its own strip instead of a second y axis, because two differently scaled axes on one plot invite false claims about co-movement. Hard to read for co-movement by eye, so it is backup, not main. |
| Rate scatter (backup) | One dot per month, rate vs share, two colors for before and after 2023. Position on both axes. It makes the correlation split (0.82 vs 0.09) visible. |
| Integrity checks | We report r for the whole period (0.48) and split it, because a single number hides that one episode drives it. We say correlations are not tested for significance and the months are not independent. |

---

## Dashboard and story (Tableau)

| Item | Decision |
|---|---|
| Structure | Linked views on one dashboard, tied together by a **filter action** on the disruption window. Click a gray band in the pressure line and the other views narrow to that window. This follows overview, then zoom and filter, then details on demand. |
| Why these views | Pressure (how bad), lane share (where it went), ports (who got hit), all on the same month axis so the eye can scan down one date. |
| Layout | Fixed size to control the layout. Time-series views stacked on a shared axis; the map has its own panel because it has no time axis. |
| Story | A guided sequence that follows the narrative: four episodes on one timeline, then the West Coast jam, then the canal and Red Sea window, then 2026. Dashboards explore; stories guide. |

---

## Chart-by-chart checklist (answer the professor's six questions)

For each chart, be ready to answer in one sentence each:

1. **Why this encoding?** (position for numbers, color only for lane.)
2. **What task does it support?** (trend, compare, extreme, locate, co-movement.)
3. **What conclusion is fair?** (pattern across four episodes, China-origin only.)
4. **How did we check integrity?** (shared definitions, honest baselines, wording corrected after checking.)
5. **What alternative did we reject, and why?** (dual axis, choropleth, color per episode, stacked area, Mexico as a proxy.)
6. **What could still mislead?** (four episodes only, overlapping windows, correlation is not cause.)
