# Final presentation script (v2, in person)

**Format:** 7 minutes talking, 3 minutes Q&A. Presentations are in person (Dec 3). Everyone attends both sessions.

**Plan:** about 6 minutes spoken, which leaves a minute of slack. Pace is about 150 words a minute. Practice once with a timer and cut a sentence if you run long.

**Who speaks:** Jason (slides 2 and 4), Paven (slides 3 and 5), Supriya (slide 6), Raul (slide 7 and the close).

**Hand-offs:** end each part by naming the next speaker ("Paven, over to you"). Whoever is not speaking stays still and looks at the slide, not at their phone.

| Slide | Speaker | Time | Running total |
|---|---|---|---|
| 1 Title | none | 0:05 | 0:05 |
| 2 The question | Jason | 0:35 | 0:40 |
| 3 Data and routes | Paven | 0:40 | 1:20 |
| 4 Pressure (Q1) | Jason | 1:00 | 2:20 |
| 5 Lanes (Q2) | Paven | 1:00 | 3:20 |
| 6 Ports (Q3) | Supriya | 1:00 | 4:20 |
| 7 Synthesis (Q4) | Raul | 1:05 | 5:25 |
| 8 Limits, conclusion, thanks | Raul | 0:35 | 6:00 |

**Rules for the whole talk (the course is Data Visualization, so the charts are the stars):**

1. On every chart slide, say three things in this order: **how to read it** (what is on each axis, what a line or circle is), **why we drew it this way**, **what it shows**.
2. Use plain words. Say "pressure score," not "standard deviations." Say "ships waiting," not "backlog."
3. Point at the chart when you say a number.
4. The color key never changes: **blue = short Pacific route, orange = longer canal route, gray shading = a disruption.**

---

## Slide 1: Title
**On screen:** Global Supply Chain Resilience, CIS 9655, the four names.
**Speaker:** none. Jason starts as soon as the slide is up. If you want, thank Prof. Santa-Coloma in one line.

---

## Slide 2: The question
**Speaker: Jason** (about 35s, 90 words)

**On screen:** "Is the supply-chain crisis actually over?" The four questions with owners. A small color key (blue, orange, gray).

**Say:**
> "Everyone remembers 2021: ships stuck outside Los Angeles, prices through the roof. The New York Fed's pressure score says supply chains are still more stretched than normal today. So our question is simple: is the crisis over, or is a new one starting? We split it into four pieces. I cover how much pressure there is. Paven covers where cargo goes. Supriya covers which ports get hit. Raul pulls it together. One thing to know before we start: in every chart, blue is the short route across the Pacific, orange is the longer route through the Panama Canal, and gray shading marks a disruption."

---

## Slide 3: Data and routes
**Speaker: Paven** (about 40s, 100 words)

**On screen:** Three data sources, the route map, two route groups, one line on China-only, one line on Mexico.

**Say:**
> "We used three real datasets: the Fed's pressure score, US Customs records of what comes in through each port, and a transportation feed of ships waiting outside ports. This map shows the idea. Cargo from China can reach the US two ways. Blue is the short way, straight across the Pacific to West Coast ports. Orange is the long way, through the Panama Canal to East and Gulf Coast ports, almost twice as far. We follow China-origin cargo, because that is where this choice exists. We also tried Mexico as a stand-in for canal traffic and dropped it, because about 90 percent of that trade moves by truck and rail, not ship."

---

## Slide 4: Q1, Pressure
**Speaker: Jason** (about 60s, 150 words)

**On screen:** Title "The pressure score is still above normal." The line chart. Three numbers: 4.43, 0.20, 1.81 (peak) and 1.28 (September).

**Say:**
> "This is a line chart of the pressure score, one point per month. Left to right is time. Up means more pressure. Zero is normal, and the dashed line at one means clearly stressed. We used one line because our question is how pressure changes over time, and we shaded every disruption the same gray, so your eye follows the line and not a rainbow of colors. Look at 2021 and 2022: the score hit 4.43 in December 2021 and stayed above one for two straight years. Now look at the Panama drought and the Red Sea bands: barely a bump, about 0.2. Real problems, but narrow. Now look at the right edge: in 2026 the score peaked at 1.81 in May, about 40 percent of the 2021 peak, and was still 1.28 in September."

*(If asked: 1.28 in September is about 29 percent of the 2021 peak. The 40 percent figure is for the 2026 peak of 1.81.)*

---

## Slide 5: Q2, Lanes
**Speaker: Paven** (about 60s, 150 words)

**On screen:** Title "Cargo shifts, but the direction depends on the disruption." Two-line chart. Two numbers: 28.3% to 36.7%, and 31.3% to 31.3%. Caveat: China-origin only.

**Say:**
> "This chart sits on the same timeline and uses the same gray bands, so you can read it right under the last one. Each line is a share: of all the cargo value we track from China, what percent lands at East and Gulf ports, in orange, versus West Coast ports, in blue. We used two lines because the question is how two groups compare over time. Watch the 2021 and 2022 band. The orange share rose from 28.3 to 36.7 percent, about eight points. Cargo moved east, away from the jam. Now the Panama drought: flat, 31.3 percent before and after. The small drop of about two points comes later, in the Red Sea window, so we do not blame the canal. One caveat: this is China-origin cargo only."

---

## Slide 6: Q3, Ports
**Speaker: Supriya** (about 60s, 150 words)

**On screen:** Title "Where the rerouted cargo landed." Backlog line chart on the left, circle map on the right. One caption line about the 103 ships.

**Say:**
> "Two views. On the left, a line chart of ships waiting for a berth: blue is Los Angeles and Long Beach, orange is Savannah, gray is every other port. In January 2022, 103 ships were waiting at Los Angeles and Long Beach, more than at all the other ports. Savannah peaked later, at 39 ships in August 2022, after the rerouted cargo arrived. On the right, a map. Each circle is a port, placed where it really is. Circle size shows how far that port's volume fell below its 2019 level at the low point. We used size because wait counts exist for only two ports, and we did not want to fake precision. The biggest circles are on the West Coast. Los Angeles and Long Beach bounced back within three months. Oakland and Seattle-Tacoma took sixteen months each, and Seattle-Tacoma then slipped again. It is the one port still clearly below 2019."

---

## Slide 7: Q4, Synthesis (the scorecard)
**Speaker: Raul** (about 65s, 165 words)

**On screen:** Title "Port jams push cargo east. Chokepoints push it west." The episode scorecard: four rows (the four disruptions), three columns of bars (pressure, cargo shift, ships waiting). A short note on shipping prices.

**Say:**
> "This is the whole project on one page. Each row is a disruption. Each column is something we measured: pressure, how far cargo moved east or west, and how many ships waited at Los Angeles and Long Beach. Longer bar, bigger number, so you can read across a row. Top row, the 2021 jam: pressure 4.43, cargo moved east by 8 points, about 41 ships waiting on average. A big jam, and cargo went east. Next two rows, the canal drought and the Red Sea: small pressure, almost no waiting, and cargo flat or drifting west. Last row, 2026: pressure up, almost no ships waiting, cargo leaning west. So there are two patterns: a port jam pushes cargo east, and a chokepoint problem pushes it west. 2026 so far looks like the second one. We also tested shipping prices as a predictor. They matched through 2022, but not since, so we do not use them to forecast."

*(Backup slides B1 to B4 hold the stacked-strips chart, the price scatter, the port-volume small multiples, and a plain-English glossary. Do not open them unless asked.)*

---

## Slide 8: Limits, conclusion, thank you
**Speaker: Raul** (about 35s, 90 words)

**On screen:** Three limits, a bottom-line box, "Thank you. Questions?", the repo link.

**Say:**
> "Three honest limits. We have only four disruptions, so this is a pattern to watch, not a law. Two of the four overlap in time. And our trade data is China only. So here is our answer: the crisis is not over, but it is not 2021 again. Pressure is still above normal, the ports are clear, and cargo is leaning back west. Which route holds up next depends on the kind of disruption. Our next step is to repeat this for a second country. Thank you. We are happy to take questions."

---

## In-person checklist (Dec 3)

- [ ] One person brings the laptop with the adapter (USB-C to HDMI) **and** a second person has the deck on their own laptop.
- [ ] Offline copy: PDF of the deck on a USB stick and in Drive, in case the room Wi-Fi fails. The web deck needs internet for its fonts and libraries.
- [ ] Open the deck on the room's projector before class if the room is free. Check that the colors and small text are readable from the back.
- [ ] Speaker notes: press **S** in the deck to open the notes window on the laptop, and drag the main slide to the projector.
- [ ] Decide who advances slides (one person with the clicker or keyboard) so nobody fights over the arrow keys.
- [ ] Screenshots of every Tableau view on a USB stick, in case Tableau Public is slow.
- [ ] Everyone has read `plain_english_faq.md` and `qa_prep_sheet.md`. Any of us may get any question.
- [ ] Time yourselves once out loud on Dec 1 or earlier. Target 6:00.
