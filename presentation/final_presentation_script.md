# Final presentation script (v4: Raul presents the deck, each teammate presents a Tableau view)

**Format:** 7 minutes talking, 3 minutes Q&A. Raul presents the deck (title, business question, data definitions, routes and episodes, hand-off). Then Jason, Paven, Supriya and Raul each present their own part of the Tableau Story. Raul comes back to the deck for the closing slide. Everyone attends both sessions (Dec 1 on Zoom, Dec 3 in person).

**Plan:** about 6:50 spoken, which leaves about 0:10 for clicks and hand-offs. Pace is about 150 words a minute. About 60% of the talk (4:04) is inside Tableau, above the course's "at least half" requirement. Practice once with a timer. If you run long, cut in this order: the last sentence of Story 3, the caution on slide 3, the title line.

**Who speaks:** Raul (slides 1 to 5, Stories 4 and 5, slide 6), Jason (Story 1), Paven (Story 2), Supriya (Story 3).

**Each Story part covers three things, in this order:** (1) the **analytical question** the view answers, (2) **how the visualization answers it**, (3) the **design decisions** that make it effective. The full detail for each person, with numbers and likely questions, is in [`story_speaker_notes.md`](story_speaker_notes.md).

**Hand-offs:** end each part by naming the next speaker. Whoever is not speaking looks at the screen, not at their phone. Raul drives the clicks the whole time, so nobody fights over the mouse. The speaker says "next" or "switch the toggle" and Raul does it.

| Part | Speaker | Time | Running total |
|---|---|---|---|
| Title | Raul | 0:07 | 0:07 |
| The question | Raul | 0:37 | 0:44 |
| Data and definitions | Raul | 0:42 | 1:26 |
| Routes and episodes | Raul | 0:33 | 1:59 |
| Hand-off to the Story | Raul | 0:14 | 2:13 |
| Story 1: Pressure | Jason | 0:54 | 3:07 |
| Story 2: Lanes | Paven | 0:50 | 3:57 |
| Story 3: Ports | Supriya | 1:05 | 5:02 |
| Story 4: Scorecard | Raul | 0:53 | 5:55 |
| Story 5: Summary | Raul | 0:22 | 6:17 |
| Limits, answer, thanks | Raul | 0:33 | 6:50 |

**Rules for the whole talk (the course is Data Visualization, so the charts are the stars):**

1. On every Story view, say three things in this order: **the question**, **how the chart answers it** (what is on each axis, what a line or circle is), **the design choices**. Then say what it shows.
2. Use plain words. Say "pressure score," not "standard deviations." Say "ships waiting," not "backlog."
3. Point at the chart when you say a number.
4. The color key never changes: **blue = short Pacific route, orange = longer Panama route, gray shading = an episode.**
5. Do not explain how we built it. The professor wants the visualization, not the process.

---

# Part 1: The deck (Raul)

## Slide 1: Title
**Speaker: Raul** (about 7s, 18 words)

**On screen:** Project title and the four names.

**Say:**
> "Good morning. We are Jason, Paven, Supriya, and Raul, and our project is on global supply chain resilience."

---

## Slide 2: The question
**Speaker: Raul** (about 37s, 92 words)

**On screen:** "Is the supply-chain crisis actually over?" Three boxes (2021, 2026, why it matters) and the four questions with owners.

**Say:**
> "Everyone remembers 2021: ships stuck outside Los Angeles, prices through the roof. In 2026 the New York Fed's pressure score is back above one, which means clearly stressed. So our business question is: is the supply chain crisis over, or is a new one starting? It matters because a port jam and a cost shock need different responses. We split it into four questions. Jason asks how much pressure there is compared with past disruptions. Paven asks whether cargo changes routes. Supriya asks which ports got hit. I pull the answer together."

---

## Slide 3: Data and definitions
**Speaker: Raul** (about 42s, 105 words)

**On screen:** Four boxes: pressure score, route share, loaded imports index, ships waiting. One note on the congestion caution.

**Say:**
> "Three real datasets, four terms. The pressure score, from the New York Fed: zero is an average month, one is clearly stressed. Route share, from US Customs port records: the percent of China's container cargo value that lands at West Coast ports versus East and Gulf ports. The loaded imports index, from the Transportation Department: containers arriving at a port compared with that port's own 2019 average, set to 100. And ships waiting for a berth, counted only for Los Angeles-Long Beach, Savannah, and all other ports together. One caution: fewer imports is not the same as congestion, because weaker demand shows up there too."

---

## Slide 4: Routes and episodes
**Speaker: Raul** (about 33s, 82 words)

**On screen:** The route map, the four episodes with dates, and the color key.

**Say:**
> "Cargo from China reaches the US two ways. Blue is the short way, straight across the Pacific to West Coast ports. Orange is the long way, through the Panama Canal to East and Gulf ports. We use China because it was the top source of US imports through 2022. We study four episodes: the 2021 port jam, the Panama drought, the Red Sea rerouting, and 2026. Two overlap. The colors never change: blue is Pacific, orange is Panama, gray is an episode."

---

## Slide 5: Hand-off to the Story
**Speaker: Raul** (about 14s, 36 words)

**On screen:** The five story points with owners and headlines, and the Tableau Public link.

**Do:** Switch to the browser tab with the Tableau Public Story (already open on point 1). Keep the deck tab open for slide 6.

**Say:**
> "Now the Tableau Story. Each of us takes one view and covers three things: the question it answers, how the chart answers it, and the design choices that make it easy to read. Jason, pressure first."

---

# Part 2: The Tableau Story (each person presents their own view)

Each story point has a headline in the box at the top. Raul clicks to the next point when the speaker says "next" or names the next speaker. Hover only where a cue says to.

## Story 1: Pressure (Jason). Headline: "2021 peaked; but there is still pressure."
**Speaker: Jason** (about 54s, 135 words)

**Do:** Point at the "Dec 2021 peak: 4.43" label, then sweep right to the 2026 line.

**Say:**
> "My question: how stretched is the supply chain now, compared with past disruptions? A line chart answers it. Time runs left to right, and height is pressure, the easiest thing for the eye to compare. Zero is a normal month, and the dashed line at one is clearly stressed. Design choices: one dark line, so the trend leads; every episode is the same gray band, labeled by name, so there is no color legend to decode; and the pandemic spike is labeled, so nobody wonders why it is not one of our four. What it shows: pressure peaked at 4.43 in December 2021. The canal drought and the Red Sea barely moved it, about 0.2. In 2026 it peaked at 1.81 in May, about 40 percent of that, and was still 1.28 in September. Paven?"

---

## Story 2: Lanes (Paven). Headline: "Congestion moved cargo east."
**Speaker: Paven** (about 50s, 126 words)

**Do:** Trace the orange rise inside the first gray band, then the flat orange line through the second band.

**Say:**
> "My question: when something goes wrong, does cargo change routes, and which way? Two lines answer it: blue is the share of China's container cargo value landing at West Coast ports, orange is the share at East and Gulf ports. Design choices: the same timeline and gray bands as the pressure chart, so your eye drops straight from one to the other; the route colors from the map; and three-month averages, so one noisy month does not look like a trend. What it shows: in the 2021 to 2022 jam, orange rose from 28 to nearly 37 percent, about eight points. Cargo moved east. In the canal drought, orange ended where it started, 31.3 percent, so the drought alone did not move cargo. China only. Supriya?"

---

## Story 3: Ports (Supriya). Headline: "West Coast ports slumped hardest."
**Speaker: Supriya** (about 65s, 163 words)

**Do:** Hover over the Seattle-Tacoma circle (low 71, latest 78). Point at the 78 on the right chart. Then click **Ships Awaiting a Berth** in the toggle and point at the LA-Long Beach peak. Leave it there and move on.

**Say:**
> "My question: which ports were hit hardest, and where do they stand now? Two views answer it. On the left, a map: each circle is a port, and a bigger circle means a bigger drop in loaded containers below that port's own 2019 level. Color is the route. On the right, the same ports as two lines, where 100 is the 2019 level. Four design choices. Each port is compared with itself, so big and small ports share one scale. Los Angeles and Long Beach share one label. Exact numbers sit in the tooltip, so the map stays clean. And a toggle swaps the right chart to ships waiting, without adding a second chart. What it shows: Seattle-Tacoma, Oakland, and Los Angeles-Long Beach fell furthest. The West Coast bottoms out at 78 in March 2023, while East and Gulf stays above 100. On the toggle, Los Angeles-Long Beach peaked at 103 ships in January 2022. Savannah peaked at 39 in August 2022. Raul?"

---

## Story 4: Scorecard (Raul). Headline: "Port jams push cargo east. Chokepoints push it west."
**Speaker: Raul** (about 53s, 133 words)

**Do:** Run a finger across the top row, then down the middle column.

**Say:**
> "My question: do the four episodes share a pattern? One table of bars answers it. Each row is an episode, each column a measure: peak pressure, cargo shift, and ships waiting at Los Angeles-Long Beach. Design choices: bar length, because length is easy to compare; rows in time order; a zero line on the cargo column; and orange for east, blue for west, matching the route colors. What it shows: 2021 has pressure 4.43, cargo east by 8.4 points, and about 41 ships waiting. The canal drought and Red Sea: pressure near 0.2, almost no waiting, cargo flat or west. 2026: pressure 1.81, almost no waiting, cargo west by 2.7 points. A port jam pushes cargo east. A chokepoint problem pushes it west. Two episodes overlap, so this is a pattern, not proof."

---

## Story 5: Summary (Raul). Headline: "2026 is a cost shock with clear ports."
**Speaker: Raul** (about 22s, 54 words)

**Do:** Point at the three takeaways on the right as you read them. Then switch back to the deck tab.

**Say:**
> "Last, the summary. The pressure and lane timelines are stacked on the same dates, so you can scan down any month. Three takeaways: 2021, extreme pressure and cargo moved east. 2023 to 2024, chokepoints, low pressure, cargo moved west. 2026, a cost shock, not a port jam. Back to the deck for our answer."

---

# Part 3: Close (Raul)

## Slide 6: Limits, answer, thanks
**Speaker: Raul** (about 33s, 83 words)

**On screen:** Three limits, the answer box, our untested theory, thank you, and the Tableau and repo links.

**Say:**
> "Three limits. Four episodes is a small sample, so this is a pattern, not proof. Two of them overlap. And our trade data is China only, about 8 percent of US goods imports this year. So our answer: the crisis is not over, but it is a different crisis. 2021 was a port jam. 2026 is a cost shock. Outside reporting points to the Middle East war and tariffs, a theory we did not test. Thank you. We are happy to take questions."

---

## Notes you can use if asked (not part of the 7 minutes)

- **2020 spike (3.47 in April 2020):** the pandemic demand shock, not one of our four freight disruptions. It is annotated on the chart so nobody wonders.
- **Why no Mexico:** about 90% of its trade moves by truck and rail, so it cannot show a sea-route choice.
- **Oct 2025 gap on the ships chart:** the Transportation Department reported no data that month, and the chart labels it.
- **Backup slides B1 to B4** in the web deck (stacked strips, shipping price scatter, port volume small multiples, glossary). Do not open them unless asked.

## In-person and Zoom checklist

- [ ] **Two browser tabs ready, in this order:** the web deck (https://raulsolanavarro.github.io/cis9655-supply-chain/) and the Tableau Story (https://public.tableau.com/views/SupplyChainResilience-Team/Story). Open both before class, click Story point 1, and test the toggle on point 3 once.
- [ ] **One driver (Raul).** Same laptop for the whole talk. A second person has both links open on their own laptop as a backup.
- [ ] **Zoom (Dec 1):** share the whole browser window (not a single tab) so you can switch between the deck and Tableau. Turn off notifications first.
- [ ] **In person (Dec 3):** laptop, the USB-C to HDMI adapter, and the deck on a second laptop. Join the room Wi-Fi early. Both pages need internet.
- [ ] **Offline fallback:** a PDF of the deck, plus one screenshot of each of the five Story points, on a USB stick and in Drive. If Tableau Public is slow, show the screenshots and keep talking.
- [ ] **Second fallback:** the file `tableau/team/Supply Chain Resilience - Team.twbx` open in Tableau Public Desktop on the driver's laptop.
- [ ] **Speaker notes:** press **S** in the web deck to open the notes window on the laptop, and drag the main slide to the projector. The deck notes are Raul's lines. Jason, Paven and Supriya use their sections of `story_speaker_notes.md`.
- [ ] Everyone has read `story_speaker_notes.md`, `qa_prep_sheet.md` and `plain_english_faq.md`. Any of us may get any question.
- [ ] Time yourselves once out loud before the session. Target 6:50.
