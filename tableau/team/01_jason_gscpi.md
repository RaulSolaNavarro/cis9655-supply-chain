# Jason: pressure index line

**What you are building:** one line showing the NY Fed pressure score from 2019 to now, with gray bands marking the four disruptions.
**Your data file:** [`gscpi_tableau.csv`](https://github.com/RaulSolaNavarro/cis9655-supply-chain/blob/main/tableau/data/gscpi_tableau.csv) (click the download icon on that page).
**Publish it as:** `GSCPI - Jason`

Read [README.md](README.md) first if you have not installed Tableau Public.

---

## Level 1: the line (5 minutes)

1. Open **Tableau Public**.
2. On the left, under **Connect**, click **Text file**.
3. Pick `gscpi_tableau.csv`.
4. Click **Sheet 1** (bottom left).

*You should see:* a blank sheet. On the left, a list of fields (date, gscpi_value, and a few more).

5. Drag **date** into the **Columns** box at the top.
6. Click the small down arrow on the green **YEAR(date)** pill. In the menu, pick the **second** "Month" option, the one that shows an example like "May 2015".

*You should see:* the pill now reads **MONTH(date)** and is green.

7. Drag **gscpi_value** into the **Rows** box.
8. In the Marks box (left middle), click **Color**. Click the color square. Click **More Colors**. Pick **RGB** and type 42, 120, 214. Click OK.

*You should see:* one blue line that spikes in 2021.

9. Double-click the sheet title. Type `Supply chain pressure (GSCPI)`. Click OK.
10. Right-click the left axis, choose **Edit Axis**, and set the title to `Std. dev. from long-run average`.

**Stop here if you are short on time. Save and publish (see README).**

---

## Level 2: the gray bands (8 minutes)

11. Drag **window_band** into **Rows**, to the right of the gscpi_value pill.
12. Right-click the new **SUM(window_band)** pill. Choose **Measure (Sum)**, then **Maximum**.

*You should see:* a second chart under the first.

13. Right-click the **MAX(window_band)** pill and choose **Dual Axis**.

*You should see:* both drawn on one chart.

14. In the Marks box, click the **MAX(window_band)** tab. Change the type from Automatic to **Bar**.
15. Click **Color**, pick RGB 217, 216, 211. Slide **Opacity** to 45%. Set **Border** to None.
16. Click **Size** and drag the slider all the way to the right.

*You should see:* solid gray bands behind the line, covering the four disruption periods.

17. Right-click the **right-hand axis**, choose **Edit Axis**, set **Fixed** start 0 and end 1. Close the box.
18. Right-click the right-hand axis again and uncheck **Show Header**.
19. Right-click the right-hand axis area and choose **Move marks to back**. If you do not see that option, skip it.
20. Do **not** choose "Synchronize Axis."

*You should see:* the blue line on top of gray bands, with no second axis showing.

---

## Level 3: labels and reference lines (5 minutes)

21. Click the **All** tab in the Marks box. Drag **disruption_window** onto **Detail**, then drag it onto **Tooltip** too.

*You should see:* hovering over a band shows its name.

22. At the top left, click the **Analytics** tab. Drag **Reference Line** onto the chart and drop it on **Table**.
23. In the box that opens: **Value** = Constant, type `0`. **Label** = None. Click OK.
24. Repeat. This time type `1`, and set the line to **dashed**. This line means "clearly stressed."
25. For each gray band, right-click inside it, choose **Annotate**, then **Area**, and type the name: `West Coast port congestion`, `Panama Canal drought`, `Red Sea / Suez rerouting`, `2026 pressure`.

---

## Publish

Follow **When you finish** in [README.md](README.md). Send the group chat the link and a screenshot.
