# Final presentation script (v3: short deck plus Tableau Story)

**Format:** 7 minutes talking, 3 minutes Q&A. The talk has two parts: a short deck that sets up the business question and the data definitions (about 2 minutes), then the Tableau Story (about 4 minutes), then one closing slide. Everyone attends both sessions (Dec 1 on Zoom, Dec 3 in person).

**Plan:** about 6:47 spoken, which leaves about 0:13 of slack. Pace is about 145 words a minute. Practice once with a timer. If you run long, cut the last sentence of Story 3 first, then the caution on slide 3. About 60% of the talk (4:05) is spent inside Tableau, above the course's "at least half" requirement.

**Who speaks:** Jason (slide 2, Story 1), Paven (slides 3 and 4, Story 2), Supriya (Story 3), Raul (slide 5, Stories 4 and 5, the close).

**Hand-offs:** end each part by naming the next speaker. Whoever is not speaking stays still and looks at the screen, not at their phone. One person (Raul) drives the clicks the whole time, so nobody fights over the mouse. The speaker says "next" or "switch the toggle" and Raul does it.

| Part | Speaker | Time | Running total |
|---|---|---|---|
| Title | none | 0:05 | 0:05 |
| The question | Jason | 0:38 | 0:43 |
| Data and definitions | Paven | 0:42 | 1:25 |
| Routes and episodes | Paven | 0:32 | 1:57 |
| How the Story works | Raul | 0:10 | 2:07 |
| Story 1: Pressure | Jason | 0:55 | 3:02 |
| Story 2: Lanes | Paven | 0:48 | 3:50 |
| Story 3: Ports | Supriya | 1:05 | 4:55 |
| Story 4: Scorecard | Raul | 0:52 | 5:47 |
| Story 5: Summary | Raul | 0:25 | 6:12 |
| Limits, answer, thanks | Raul | 0:35 | 6:47 |

**Rules for the whole talk (the course is Data Visualization, so the charts are the stars):**

1. On every chart, say three things in this order: **how to read it** (what is on each axis, what a line or circle is), **why we drew it this way**, **what it shows**.
2. Use plain words. Say "pressure score," not "standard deviations." Say "ships waiting," not "backlog."
3. Point at the chart when you say a number.
4. The color key never changes: **blue = short Pacific route, orange = longer Panama route, gray shading = an episode.**
5. Do not explain how we built it. The professor wants the visualization, not the process.

---

## Slide 1: Title
**Speaker:** none. Jason starts as soon as the slide is up. If you want, thank Prof. Santa-Coloma in one line (about 5 seconds).

---

## Slide 2: The question
**Speaker: Jason** (about 38s, 85 words)

**On screen:** "Is the supply-chain crisis actually over?" Three boxes (2021, 2026, why it matters) and the four questions with owners.

**Say:**
> "Everyone remembers 2021: ships stuck outside Los Angeles, prices through the roof. In 2026 the New York Fed's pressure score is back above one, which means clearly stressed. So our question is simple: is the crisis over, or is a new one starting? It matters because a port jam and a cost shock need different responses. We split the question into four. I cover how much pressure there is. Paven covers whether cargo changes routes. Supriya covers which ports got hit. Raul pulls it together."

---

## Slide 3: Data and definitions
**Speaker: Paven** (about 42s, 101 words)

**On screen:** Four boxes: pressure score, route share, loaded imports index, ships waiting. One note on BTS and the congestion caution.

**Say:**
> "We used three real datasets and four terms. The pressure score: zero is an average month, one is clearly stressed. Route share, from US Customs records: the percent of China's container cargo that lands at West Coast ports versus East and Gulf ports. The loaded imports index, from the Transportation Department: containers arriving at a port compared with that port's own 2019 average, set to 100. And ships waiting for a berth, counted only for Los Angeles-Long Beach, Savannah, and all other ports together. One caution: fewer imports is not the same as congestion, because weaker demand shows up there too."

---

## Slide 4: Routes and episodes
**Speaker: Paven** (about 32s, 75 words)

**On screen:** The route map, the four episodes with dates, and the color key.

**Say:**
> "Cargo from China reaches the US two ways. Blue is the short way across the Pacific to West Coast ports. Orange is the long way through the Panama Canal to East and Gulf ports, almost twice as far. We use China because it was the top source of US imports through 2022. We study four episodes, and two of them overlap. The colors never change: blue is Pacific, orange is Panama, gray is an episode."

---

## Slide 5: How the Story works
**Speaker: Raul** (about 10s, 16 words)

**On screen:** The five story points with owners and headlines, and the Tableau Public link.

**Do:** Raul switches to the browser tab with the Tableau Public Story (already open, on point 1). Keep the deck tab open for slide 6.

**Say:**
> "From here we are in Tableau. Five story points, same colors throughout. Jason, over to you."

---

# The Tableau Story

Each story point has a headline in the box at the top. Click the next box (or the right arrow) to move on. Hover for tooltips only where a cue below says to.

## Story 1: Pressure (headline: "2021 peaked; but there is still pressure.")
**Speaker: Jason** (about 55s, 130 words)

**Do:** Point at the "Dec 2021 peak: 4.43" label, then sweep right to the 2026 line. Hover over the May 2026 peak if the tooltip works.

**Say:**
> "This is a line chart of the pressure score, one point per month. Left to right is time. Up means more pressure. Zero is a normal month, and the dashed line at one means clearly stressed. We used one line because the question is how pressure changes over time, and every episode is the same gray, so your eye follows the line. The score peaked at 4.43 in December 2021, in the port-congestion episode. The 2020 spike is the pandemic, which is not one of our four. Now look at the canal drought and Red Sea bands: barely a bump, about 0.2. On the right, 2026 peaked at 1.81 in May, about 40 percent of the 2021 peak, and was still 1.28 in September. So there is still pressure. Paven?"

---

## Story 2: Lanes (headline: "Congestion moved cargo east.")
**Speaker: Paven** (about 48s, 115 words)

**Do:** Click to point 2. Trace the orange rise inside the first gray band, then the flat line through the second band.

**Say:**
> "Same timeline, same gray bands. Each line is a share: of the cargo value we track from China, what percent lands at West Coast ports, in blue, versus East and Gulf ports, in orange. We used two lines because we are comparing two groups over time. In the 2021 to 2022 congestion band, orange rose from 28 to nearly 37 percent, about eight points. Cargo moved east, away from the jam. In the Panama drought band, orange ended exactly where it started, at 31.3 percent, so the drought alone did not move cargo. The small drop of about two points comes later, in the Red Sea window. One caveat: this is China-origin cargo only. Supriya?"

---

## Story 3: Ports (headline: "West Coast ports slumped hardest.")
**Speaker: Supriya** (about 65s, 157 words)

**Do:** Click to point 3. Hover over the Seattle-Tacoma circle (low 71%, now 78%). Point at the 78 on the right chart. Then click **Ships Awaiting a Berth** in the toggle and point at the LA-Long Beach peak. Leave it on that view and move on.

**Say:**
> "Two views of the ports. On the left, a map. Each circle is a port. Its size shows how far that port's loaded imports fell below its own 2019 level at the low point in 2022 and 2023. Bigger circle, bigger drop. Color is the route: blue Pacific, orange Panama. The big blue circles are Seattle-Tacoma, Oakland, and Los Angeles-Long Beach. Houston and Charleston never dipped, so their circles are tiny. Hover on a circle to see a port's low and where it stands today. On the right, the same ports averaged into two lines, West Coast and East and Gulf. 100 is the 2019 level. The West Coast bottoms out at 78 in March 2023, while East and Gulf stays above 100. Now switch the toggle to ships waiting for a berth. Los Angeles-Long Beach peaked at 103 ships in January 2022. Savannah peaked later, at 39 in August 2022, after the rerouted cargo arrived. Raul?"

---

## Story 4: Scorecard (headline: "Port jams push cargo east. Chokepoints push it west.")
**Speaker: Raul** (about 52s, 121 words)

**Do:** Click to point 4. Run a finger across the top row, then down the middle column.

**Say:**
> "This is the whole project on one page. Each row is an episode. Each column is something we measured: peak pressure, how far cargo moved, and how many ships waited at Los Angeles-Long Beach. Orange means cargo moved east, blue means west. Top row, the 2021 jam: pressure 4.43, cargo moved east by 8.4 points, about 41 ships waiting. The canal drought and the Red Sea: pressure about 0.2, almost no waiting, cargo flat or drifting west. Last row, 2026: pressure 1.81, almost no waiting, cargo leaning west by 2.7 points. So there are two patterns. A port jam pushes cargo east. A chokepoint problem pushes it west. Two of these episodes overlap, so treat this as a pattern, not proof."

---

## Story 5: Summary (headline: "2026 is a cost shock with clear ports.")
**Speaker: Raul** (about 25s, 56 words)

**Do:** Click to point 5. Point at the three takeaways on the right as you read them. Then switch back to the deck tab.

**Say:**
> "Here is the whole story on one timeline. 2021: extreme pressure, and cargo moved east. 2023 to 2024: chokepoint problems, low pressure, and cargo moved west. 2026: pressure is up again, ports are clear, and cargo is leaning west. That is a cost shock, not a port jam. Now back to the deck for our answer."

---

## Slide 6: Limits, answer, thanks
**Speaker: Raul** (about 35s, 83 words)

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
- [ ] **Speaker notes:** press **S** in the web deck to open the notes window on the laptop, and drag the main slide to the projector. The notes contain the same text as this script.
- [ ] Everyone has read `plain_english_faq.md` and `qa_prep_sheet.md`. Any of us may get any question.
- [ ] Time yourselves once out loud before the session. Target 6:47.
