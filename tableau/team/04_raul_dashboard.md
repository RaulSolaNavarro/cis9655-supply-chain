# Raul: palette, dashboard, story

**What you are building:** one workbook that holds everyone's sheets, a dashboard where clicking a gray band filters the other charts, and a short story.

**Do this after** Jason, Paven, and Supriya have posted their Tableau Public links. If anyone is late, build with what you have and use their screenshot for the rest. Do not let this block the deck.

---

## Step 1: Collect the sheets (10 minutes)

1. Open each teammate's Tableau Public link in your browser.
2. Click the **download icon** at the bottom right, then **Download Workbook**. Save each file. (If the icon is missing, ask them to turn **Allow downloads** on.)
3. In Tableau Public, open **your own new workbook** (File, New). Connect the four CSVs: `gscpi_tableau.csv`, `lane_share_tableau.csv`, `port_map_tableau.csv`, `port_series_tableau.csv`. Keep them as **four separate data sources**.
4. Open each downloaded workbook in its own Tableau window.
5. In each teammate's window, **right-click a sheet tab** at the bottom, choose **Copy**. In your window, **right-click empty tab space**, choose **Paste**.

*You should see:* sheets named GSCPI, Lane share, Port map, and Port series in your workbook.

**Fast fallback:** if copying fails, build your own copy of that sheet from their guide (Level 1 is enough), or use their screenshot in the deck and skip that sheet in the dashboard.

## Step 2: The dashboard (8 minutes)

6. Menu **Dashboard**, **New Dashboard**.
7. At the bottom left, set **Size** to **Fixed size**, **1280 x 720**.
8. Drag **GSCPI** into the dashboard. Drag **Lane share** under it. Drag **Port series** under that. (Same month axis, so you scan down one date.)
9. Drag **Port map** to the right side.
10. Double-click the dashboard title and type `Global supply chain resilience, Jan 2019 to Sep 2026`.

*You should see:* three time charts stacked on the left and the map on the right.

## Step 3: The click-to-filter action (5 minutes)

11. Menu **Dashboard**, **Actions**, **Add Action**, **Filter**.
12. **Name:** `Filter by disruption window`. **Source Sheets:** GSCPI only. **Run action on:** Select. **Target Sheets:** Lane share and Port series (untick Port map). **Clearing the selection will:** Show all values.
13. Under **Target Filters**, choose **Selected Fields**, click **Add Filter**, and match `disruption_window` to `disruption_window` for each target data source. Click OK.
14. Test it: click a gray band on the GSCPI chart. The other two charts should narrow to that window. Click empty space to reset.

## Step 4: The story (5 minutes)

15. Menu **Story**, **New Story**. Size **Fixed**, 1280 x 800.
16. Drag the dashboard onto the story. Caption: `Four disruptions on one timeline`. Select nothing.
17. Click **Duplicate**. On the new point, click the West Coast band on GSCPI, then click **Update**. Caption: `West Coast jam: cargo shifted east`.
18. Duplicate again. Ctrl-click a Panama-only month and a Red Sea month, then **Update**. Caption: `Canal and Red Sea: a small drift west`.
19. Duplicate again. Click the 2026 band, **Update**. Caption: `2026: pressure up, ports clear`.

## Step 5: Publish

20. **File**, **Save to Tableau Public As...**. Name it `Global Supply Chain Resilience`.
21. Copy the link, send it to the group, and give it to Claude Code to add to slide 8 and the README.
22. Take screenshots of the dashboard and each story point. Save them in a folder named `tableau_screenshots` as a backup for Dec 3.

**Wording to keep:** the Panama drought alone left the lane share flat. The westward drop came during the Red Sea window.
