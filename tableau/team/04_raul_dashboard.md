# Raul: palette, dashboard, story

**What you are building:** one workbook that holds everyone's sheets, one dashboard per view, and a five-point story.
**Finished workbook:** [`tableau/team/Supply Chain Resilience - Team.twbx`](Supply%20Chain%20Resilience%20-%20Team.twbx). Open it to compare with what you build.

**Do this after** Jason, Paven, and Supriya have posted their Tableau Public links. If anyone is late, build with what you have and use their screenshot for the rest. Do not let this block the deck.

---

## Step 1: Collect the sheets (10 minutes)

1. Open each teammate's Tableau Public link in your browser.
2. Click the **download icon** at the bottom right, then **Download Workbook**. Save each file. (If the icon is missing, ask them to turn **Allow downloads** on.)
3. In Tableau Public, open **your own new workbook** (File, New). Connect the four CSVs: `gscpi_tableau.csv`, `lane_share_tableau.csv`, `port_map_tableau.csv`, `port_series_tableau.csv`. Keep them as **four separate data sources**.
4. Open each downloaded workbook in its own Tableau window.
5. In each teammate's window, **right-click a sheet tab** at the bottom, choose **Copy**. In your window, **right-click empty tab space**, choose **Paste**.

*You should see:* sheets named GSCPI, Lane share, Port map, and Port series in your workbook.

**Fast fallback:** if copying fails, build your own copy o## Step 2: The dashboards (10 minutes)

6. Menu **Dashboard**, **New Dashboard**.
7. At the bottom left, set **Size** to **Fixed size**, **1560 x 660**.
8. Drag **GSCPI** into it. Double-click the tab at the bottom and name it `Pressure`.
9. Repeat for **Lanes** (Lane share sheet), **Ports** (Port map and Port series side by side, keep the filter card next to the series), and **Scorecard** (the scorecard sheet).
10. Make one more called **Summary**: GSCPI and Lane share stacked on the left, and a **Text** object on the right with three takeaways (2021, 2023 to 2024, 2026).

*You should see:* five dashboard tabs: Pressure, Lanes, Ports, Scorecard, Summary.

## Step 3: The story (5 minutes)

11. Menu **Story**, **New Story**. Size **Fixed**, 1600 x 850.
12. Drag **Pressure** onto the story. Caption: `2021 peaked; but there is still pressure.`
13. Click **Blank**, drag **Lanes** in. Caption: `Congestion moved cargo east.`
14. Blank, **Ports**. Caption: `West Coast ports slumped hardest.`
15. Blank, **Scorecard**. Caption: `Port jams push cargo east. Chokepoints push it west.`
16. Blank, **Summary**. Caption: `2026 is a cost shock with clear ports.`

*You should see:* five story points across the top. Clicking each one shows its dashboard.

## Step 4: Publish

17. **File**, **Save to Tableau Public As...**. Name it `Supply Chain Resilience - Team`.
18. Copy the link, send it to the group, and give it to Claude Code to add to the deck and the README.
19. Save the workbook as `tableau/team/Supply Chain Resilience - Team.twbx` in the repo.
20. Take screenshots of each story point as a backup for Dec 3.

 screenshots of the dashboard and each story point. Save them in a folder named `tableau_screenshots` as a backup for Dec 3.

**Wording to keep:** the Panama drought alone left the lane share flat. The westward drop came during the Red Sea window.
