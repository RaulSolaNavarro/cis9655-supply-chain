# Raul: episode scorecard

**What you are building:** one chart with four rows (one per disruption) and three side-by-side bar panels: how high the pressure score got, how much the East and Gulf share moved, and how many ships waited at LA-Long Beach.
**Your data file:** [`scorecard_tableau.csv`](https://github.com/RaulSolaNavarro/cis9655-supply-chain/blob/main/tableau/data/scorecard_tableau.csv) (click the download icon on that page).
**Publish it as:** `Scorecard - Raul`

Read [README.md](README.md) first if you have not installed Tableau Public.

---

## Level 1: the scorecard (about 10 minutes)

### Connect and set up the rows

1. Open **Tableau Public**.
2. On the left, under **Connect**, click **Text file**.
3. Pick `scorecard_tableau.csv`.
4. Click **Sheet 1** (bottom left).

*You should see:* a blank sheet. On the left, a list of fields (episode, episode_order, peak_gscpi, share_change_pp, and a few more).

5. Drag **episode** into the **Rows** box.
6. Right-click the blue **episode** pill in Rows and choose **Sort...**.
7. Set **Sort By** to **Field**. Set **Sort Order** to **Ascending**. Set the field to **episode_order** and the aggregation to **Minimum**. Close the box.

*You should see:* four names down the left side, in this order from top to bottom: West Coast port congestion, Panama Canal drought, Red Sea / Suez rerouting, Renewed 2026 pressure.

### Add the three bar panels

8. Drag **peak_gscpi** into the **Columns** box.
9. Drag **share_change_pp** into **Columns**, to the right of the first pill. Drop it **next to** the first pill, not on top of it.
10. Drag **lalb_ships_waiting_mean** into **Columns**, to the right of the second pill.

*You should see:* three green pills in Columns (SUM(peak_gscpi), SUM(share_change_pp), SUM(lalb_ships_waiting_mean)), three panels side by side, each with its own axis along the bottom. The Marks box now has four tabs: **All** and one per measure.

11. In the Marks box, click the **All** tab. Change the type from Automatic to **Bar**.
12. Still on **All**, click **Label** and check **Show mark labels**.

*You should see:* horizontal bars in all three panels, each with its number at the end. The West Coast row has by far the longest bar in the first and third panels.

### Colors

13. In the Marks box, click the **SUM(peak_gscpi)** tab. Click **Color**, then **More Colors**. Pick **RGB** and type 85, 85, 85. Click OK.
14. Click the **SUM(lalb_ships_waiting_mean)** tab. Do the same: RGB 85, 85, 85.
15. Click the **SUM(share_change_pp)** tab. Drag **cargo_moved** onto **Color** in that tab only.
16. Click **Color**, then **Edit Colors...**. For each item in the list on the left, **double-click** it. A color picker opens. Type the RGB and click OK:
    - **East**: 255, 107, 53 (orange)
    - **West**: 42, 120, 214 (blue)
    - **No change**: 138, 137, 132 (gray)
17. Click OK.

*You should see:* the left and right panels in dark gray. The middle panel has an orange bar going right for West Coast congestion, blue bars going left for Red Sea and 2026, and a 0.0 label (no visible bar) for Panama. A color legend for cargo_moved appears on the right.

### Zero line

18. At the top left, click the **Analytics** tab.
19. Drag **Reference Line** onto the chart. A drop box appears with a row for each measure. Drop it on **Table** in the **SUM(share_change_pp)** row only.
20. In the box that opens: **Value** = Constant, type `0`. **Label** = None. Line color black, solid. Click OK.
21. Click back to the **Data** tab (top left).

*You should see:* a thin vertical line at zero in the middle panel only, so it is clear which bars go left and which go right.

### Plain-language headers

22. Right-click the bottom axis of the **left** panel and choose **Edit Axis...**. Set the title to `Pressure score (peak)`. Close the box.
23. Same for the **middle** panel: `East and Gulf share change (points)`.
24. Same for the **right** panel: `Ships waiting, LA-Long Beach (average)`.
25. Right-click the word **episode** above the four names and choose **Hide Field Labels for Rows**.

*You should see:* three readable titles under the three panels, and no "episode" label above the names.

### Clean up the lines

26. In the top menu, click **Format**, then **Lines...**.
27. In the panel that opens on the left, click the **Rows** tab. Set **Grid Lines** to **None**.
28. Click the **Columns** tab. Set **Grid Lines** to **None**. Close the format panel (the X at its top).

*You should see:* no gray grid lines behind the bars. The zero line in the middle panel is still there.

### Title and footnote

29. Double-click the sheet title. Delete what is there and type `Port jams push cargo east. Chokepoints push it west.` Click OK.
30. In the top menu, click **Worksheet**, then **Show Caption**.
31. Double-click the caption box (bottom of the sheet). Delete what is there and type the two notes from the **note** column:
    `Panama Canal drought and Red Sea / Suez rerouting: windows overlap Nov 2023 to May 2024. Renewed 2026 pressure: cargo shift runs through Aug 2026; pressure through Sep 2026.`
    Click OK.
32. Optional: drag **note** onto **Tooltip** on the **All** tab, so hovering a bar also shows its note.

*You should see:* the full scorecard: title on top, four rows, three bar panels, orange and blue only in the middle panel, and the footnote under the chart.

**Stop here if you are short on time. Save and publish (see Level 2).**

---

## Level 2: publish and what to say (5 minutes)

33. Rename the sheet tab (bottom) to `Scorecard`: double-click the tab and type it.
34. **File**, then **Save to Tableau Public As...**. Sign in. Name it `Scorecard - Raul`.
35. On the published page, make sure **Allow downloads** is on.

*You should see:* the scorecard in your browser at a public link. Copy the link and save a screenshot as backup.

**Three design choices to say out loud when you present it:**

1. **Length on a common baseline.** Every bar starts at the same line, so you compare lengths, which is the easiest thing for the eye to read accurately.
2. **Each panel has its own scale.** A pressure score, a share in points, and a count of ships are different units. Putting them on one axis would make the ships panel swamp the other two.
3. **Color means direction only.** Orange is cargo moving east, blue is cargo moving west, gray is no change. The other two panels stay dark gray so the color is never decoration.

---

## If it looks wrong

| What you see | Most likely cause | Fix |
|---|---|---|
| All three measures in **one** panel, with a "Measure Names" pill or colored by measure | You dropped a measure **on top of** another pill (or onto the axis) instead of next to it | Press **Ctrl+Z** until Columns is back to one pill, then drag the next measure so it lands to the **right** of the existing pill (watch for the small orange insert marker) |
| Bars are **all one color**, or all three panels are orange and blue | **cargo_moved** went onto Color in the **All** tab, or not at all | Remove it from the All tab (drag it off), click the **SUM(share_change_pp)** tab, and drop it on Color there (steps 13 to 17) |
| **Renewed 2026 pressure is on top** (order reversed) or names are alphabetical | Sort set to Descending, or sorted by episode instead of episode_order | Redo steps 6 and 7: Sort By **Field**, **Ascending**, **episode_order**, **Minimum** |
