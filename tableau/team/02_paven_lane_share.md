# Paven: lane share (two lines)

**What you are building:** two lines, one for the share of China imports landing at West Coast ports (blue), one for East and Gulf ports (orange), with the gray disruption bands behind them.
**Your data file:** [`lane_share_tableau.csv`](https://github.com/RaulSolaNavarro/cis9655-supply-chain/blob/main/tableau/data/lane_share_tableau.csv) (click the download icon on that page).
**Publish it as:** `Lane share - Paven`

Read [README.md](README.md) first if you have not installed Tableau Public.

---

## Level 1: the two lines (7 minutes)

1. Open **Tableau Public**. Under **Connect**, click **Text file** and pick `lane_share_tableau.csv`.
2. Click **Sheet 1**.
3. Drag **date** into **Columns**. Click the arrow on the green pill and pick the **second** "Month" option (the one showing "May 2015"). The pill should read **MONTH(date)**.
4. Drag **pacific_direct_share_3mo_pct** into **Rows**.
5. Drag **panama_dependent_share_3mo_pct** onto the same left axis. Release when you see a **double ruler** icon.

*You should see:* two lines on one chart. A **Measure Names** legend appears on the right.

6. Look at the **Filters** box. If it lists anything besides your two measures, click the arrow, **Edit Filter**, and uncheck the extras.
7. In the Marks box, set the type to **Line**.
8. Click the colors in the legend (right side). Double-click **pacific_direct_share_3mo_pct**, choose **More Colors**, RGB 42, 120, 214.
9. Do the same for **panama_dependent_share_3mo_pct** with RGB 235, 104, 52.
10. Right-click each legend entry, **Edit Alias**: type `Pacific-direct` and `Panama-dependent`.
11. Right-click the left axis, **Edit Axis**, set **Fixed** start 20, end 75. Title: `% of China containerized import value`.
12. Double-click the sheet title and type `China imports by lane group (3-month average)`.

*You should see:* an orange line that rises in 2021 to 2022 while the blue line dips.

**Stop here if you are short on time. Save and publish.**

---

## Level 2: the gray bands (8 minutes)

13. Drag **window_band** into **Rows**, to the right of your measures.
14. Right-click **SUM(window_band)**, **Measure (Sum)**, **Maximum**.
15. Right-click **MAX(window_band)** and choose **Dual Axis**.
16. In the Marks box, click the **MAX(window_band)** tab. Set the type to **Bar**.
17. **Color**: RGB 217, 216, 211, **Opacity** 45%, **Border** None. **Size**: slider all the way right.
18. Right-click the **right-hand axis**, **Edit Axis**, **Fixed** 0 to 1. Right-click it again, uncheck **Show Header**.
19. Do not choose Synchronize Axis.

*You should see:* gray bands behind both lines.

---

## Level 3: polish (3 minutes)

20. Click the **All** tab. Drag **disruption_window** onto **Detail** and onto **Tooltip**.
21. In the Marks box, click **Label**, tick **Show mark labels**, and choose **Line Ends** so each line is named at its right end.
22. Add a caption: **Worksheet**, **Show Caption**, type `China-origin imports only.`

---

## Publish

Follow **When you finish** in [README.md](README.md). Send the group chat the link and a screenshot.
