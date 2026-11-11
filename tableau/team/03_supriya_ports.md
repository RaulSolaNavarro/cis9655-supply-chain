# Supriya: port map and port series

**What you are building:** two sheets. (A) A map with one circle per port, sized by how far its volume fell below 2019. (B) A line chart of ships waiting or containers moved, per port.
**Your data files** (click the download icon on each page):
- [`port_map_tableau.csv`](https://github.com/RaulSolaNavarro/cis9655-supply-chain/blob/main/tableau/data/port_map_tableau.csv)
- [`port_series_tableau.csv`](https://github.com/RaulSolaNavarro/cis9655-supply-chain/blob/main/tableau/data/port_series_tableau.csv)

**Publish both sheets in one workbook as:** `Ports - Supriya`

Read [README.md](README.md) first if you have not installed Tableau Public. Do **Part A (map)** first. It is the one the deck uses.

---

# Part A: the port map

## Level 1: circles on a map (8 minutes)

1. Open **Tableau Public**. Under **Connect**, click **Text file** and pick `port_map_tableau.csv`. Click **Sheet 1**.
2. In the field list, right-click **lat**. Choose **Geographic Role**, then **Latitude**.
3. Right-click **lon**. Choose **Geographic Role**, then **Longitude**.

*You should see:* the two fields now show a small globe icon.

4. Double-click **lon**, then double-click **lat**. A map appears.
5. Drag **port** onto **Detail** in the Marks box.

*You should see:* nine dots on a US map.

6. Drag **map_marker_size** onto **Size** in the Marks box.
7. Click the **Size** button, drag the slider so the biggest circle is clearly visible but not huge. Right-click the size legend, **Edit Sizes**, and tick **Start at zero** so area stays honest.
8. Drag **lane_group** onto **Color**. Click **Edit Colors**: Pacific-direct RGB 42, 120, 214. Panama-dependent RGB 235, 104, 52.

*You should see:* big blue circles on the West Coast, smaller orange circles on the East and Gulf coasts.

9. Menu **Map**, **Background Maps**, **Light**.
10. Double-click the sheet title. Type `2022-23 import slump by port`.

**Stop here if you are short on time. Save and publish.**

## Level 2: labels and open rings (6 minutes)

11. Drag **port** onto **Label** in the Marks box.
12. Drag **dipped** onto **Shape**. Change the Marks type to **Shape**. Click **Shape**, and give `Yes` a filled circle and `No` an open circle. Charleston and Houston never fell below 2019, so they get open rings.
13. Drag these onto **Tooltip**: **slump_points**, **trough_month**, **months_to_recover**, **latest_index**.
14. Add a caption: **Worksheet**, **Show Caption**: `Circle area = points below 2019 at the 2022-23 low. A proxy: berth waits are published for only LA + Long Beach, Savannah, and all other ports.`

*Note:* Los Angeles and Long Beach sit about 8 km apart, so their circles overlap. That is normal. The tooltip separates them.

---

# Part B: the port series

## Level 1: lines by port (8 minutes)

15. In Tableau, click **New Data Source** (the cylinder icon, top left). Pick **Text file** and `port_series_tableau.csv`. Click a new sheet at the bottom (**Sheet 2**).
16. Drag **date** to **Columns**. Click its arrow and pick the **second** "Month" option. It should read **MONTH(date)**.
17. Drag **value** to **Rows**.
18. Drag **port_or_group** onto **Detail**.
19. Drag **metric_name** onto **Filters**. In the box, tick **Loaded imports index**. Click OK.
20. Right-click the new filter pill, choose **Show Filter**. Click the small arrow on the filter card and pick **Single Value (list)**.

*You should see:* a line per port. Switching the filter between **Loaded imports index** and **Ships awaiting a berth** swaps the chart.

21. Drag **lane_group** onto **Color**. Edit colors: Pacific-direct RGB 42, 120, 214. Panama-dependent RGB 235, 104, 52. All Other Ports RGB 138, 137, 132.
22. Click **Label** in the Marks box, tick **Show mark labels**, and choose **Line Ends**.

*You should see:* direct labels at the right end of each line.

## Level 2: bands (optional, 6 minutes)

23. Drag **window_band** to **Rows**. Right-click it, **Measure (Sum)**, **Maximum** (**not** Sum: there are up to 9 rows per month).
24. Right-click it, **Dual Axis**. Marks tab for MAX(window_band): **Bar**, color RGB 217, 216, 211, opacity 45%, border None, size slider all the way right.
25. Right-click the right axis, **Edit Axis**, **Fixed** 0 to 1, and uncheck **Show Header**.

---

## Publish

Follow **When you finish** in [README.md](README.md). Send the group chat the link and a screenshot of the **map** (Part A). If you only finished Part A, that is fine.
