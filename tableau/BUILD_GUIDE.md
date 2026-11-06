# Building the project in Tableau Desktop

> **The generated `supply_chain_resilience.twbx` / `.twb` is confirmed broken, not just untested.** Tableau Desktop refuses to load it (error D2E8DA72: schema errors on the `reference-line` elements and the storyboard `window` element), so don't use it or try to repair it; build from this guide.

This guide rebuilds the project's four views, a linked dashboard, and a story in Tableau Desktop in about an hour. Use it if the course deliverable has to be a Tableau workbook. It doesn't depend on `supply_chain_resilience.twbx`, which is confirmed broken: Tableau Desktop refuses to load it (see [About the .twbx](#about-the-twbx)).

**Inputs:** the four CSVs in `tableau/data/`, built by `python tableau/build_tableau_data.py` from the same loaders as the q1–q4 charts. The hard parts are precomputed (window labels, band helper, map coordinates, marker sizes), so the build below uses **no calculated fields**.

| Step | What | Time |
|---|---|---|
| 0 | Palette and data sources | 5 min |
| 1 | Sheet "GSCPI": line with window bands | 12 min |
| 2 | Sheet "Lane share": two lines with bands | 10 min |
| 3 | Sheet "Port map": symbol map from lat/lon | 10 min |
| 4 | Sheet "Port series": backlog or throughput | 8 min |
| 5 | Dashboard and filter action | 10 min |
| 6 | Story | 5 min |

Notation: **Columns** / **Rows** are the shelves; **Color**, **Size**, **Shape**, **Label**, **Detail**, and **Tooltip** are buttons on the Marks card. "Continuous month" means a green `MONTH(date)` pill: drag `date` to the shelf, right-click the pill, and pick **Month** from the *second* group (the one showing "May 2015"), not the first.

---

## 0. Palette and data sources

### Colors

These are the exact values in the q1–q4 build scripts. On Windows, Tableau's color picker takes RGB, not hex.

| Use | Hex | RGB |
|---|---|---|
| Pacific-direct, LA-LB, GSCPI line | `#2a78d6` | 42, 120, 214 |
| Panama-dependent, Savannah | `#eb6834` | 235, 104, 52 |
| All Other Ports (backlog) | `#8a8984` | 138, 137, 132 |
| Disruption-window bands (all windows), at **45% opacity** | `#d9d8d3` | 217, 216, 211 |
| Reference lines, secondary text | `#52514e` | 82, 81, 78 |
| Primary text | `#0b0b0b` | 11, 11, 11 |
| Background | `#fcfcfb` | 252, 252, 251 |

The windows are all the same gray, as in the matplotlib charts. They're told apart by labels, not color.

**Optional, saves typing:** close Tableau, open `Documents\My Tableau Repository\Preferences.tps` in a text editor, and replace its contents with the following. Then reopen Tableau. **Edit Colors → Select Color Palette** will then list "Supply chain resilience".

```xml
<?xml version='1.0'?>
<workbook>
  <preferences>
    <color-palette name="Supply chain resilience" type="regular">
      <color>#2a78d6</color>
      <color>#eb6834</color>
      <color>#8a8984</color>
      <color>#d9d8d3</color>
      <color>#52514e</color>
    </color-palette>
  </preferences>
</workbook>
```

### Connect the four CSVs

1. **Connect → To a File → Text file**, and pick `tableau/data/gscpi_tableau.csv`.
2. In the data source grid, check that `date` shows a calendar icon (Date). If it shows "Abc", click the icon and choose **Date**.
3. Repeat **Data → New Data Source** for `lane_share_tableau.csv`, `port_map_tableau.csv`, and `port_series_tableau.csv`. Keep them as **four separate data sources**. Don't join or relate them; the dashboard links them with a filter action instead.

What the columns mean (all four files):

| Column | Meaning |
|---|---|
| `disruption_window` | The window name for that month, or blank. Months where Panama and Red Sea overlap (Nov 2023 – May 2024) read `Panama Canal drought + Red Sea / Suez rerouting`. |
| `in_west`, `in_panama`, `in_red`, `in_renewed` | 1 if the month is inside that window, else 0. Use these to filter to one whole window, overlap included. |
| `window_band` | 1 inside any window, blank outside. Drives the shaded bands. |

---

## 1. Sheet "GSCPI": line with window bands

**Base line**

1. **Columns:** `date` as continuous month.
2. **Rows:** `gscpi_value` (shows as `SUM(gscpi_value)`; there's one row per month, so SUM is the value).
3. Marks card: **Line**. **Color** → `#2a78d6`.

**Window bands (dual-axis bar technique)**

4. Drag `window_band` to **Rows**, to the right of `SUM(gscpi_value)`.
5. Right-click the new pill → **Measure (Sum) → Maximum**. It now reads `MAX(window_band)`.
6. Right-click `MAX(window_band)` → **Dual Axis**.
7. On the Marks card, open the `MAX(window_band)` tab:
   - Mark type **Bar**.
   - **Color** → `#d9d8d3`, then **Color → Opacity 45%**, Border: None.
   - **Size** → drag the slider all the way right, so adjacent months touch and form solid bands.
8. Right-click the right-hand axis → **Edit Axis** → Range **Fixed**, start `0`, end `1` → OK. Right-click it again → uncheck **Show Header**.
9. Right-click the right-hand axis area → **Move marks to back**, so the line draws over the bands. If that option isn't there, drag `MAX(window_band)` to the *left* of `SUM(gscpi_value)` on Rows and redo steps 6–8 for the new right axis.
10. Do **not** synchronize the axes. The band axis must stay 0–1.

**Fields the filter action needs**

11. Open the **All** tab of the Marks card and drag `disruption_window` onto **Detail**. Also drag it onto **Tooltip**. Without it on Detail, clicking a mark can't pass the window to other sheets.

**Reference lines and labels**

12. **Analytics** pane → drag **Reference Line** onto the chart → **Table**, axis `SUM(gscpi_value)`, Value **Constant `0`**, Label None, line `#52514e` solid. Repeat with **Constant `1`**, dashed. That's the "+1 std. dev., elevated" line.
13. Left axis title: `Std. dev. from long-run average`. Sheet title: `Supply chain pressure (GSCPI)`.
14. Window labels: right-click a band near the start of each window → **Annotate → Area**. Type `West Coast port congestion`, `Panama Canal drought`, `Red Sea / Suez rerouting`, and `2026 pressure`, and drag each to sit at the top of its band.

---

## 2. Sheet "Lane share": two lines with bands

1. Data source: `lane_share_tableau`. **Columns:** `date` as continuous month.
2. **Rows:** `pacific_direct_share_3mo_pct`. Then drag `panama_dependent_share_3mo_pct` **onto the existing axis** and release when the double-ruler icon appears. Tableau switches to `Measure Values` on Rows and puts `Measure Names` on Color.
3. **Filters** shelf: `Measure Names` should keep only those two measures. Edit the filter and uncheck anything else.
4. **Color** (`Measure Names`) → Edit Colors: Pacific-direct `#2a78d6`, Panama-dependent `#eb6834`. Right-click each legend item → **Edit Alias** → `Pacific-direct` and `Panama-dependent`.
5. Mark type **Line**. Left axis: Edit Axis → Fixed `20` to `75`, title `% of China containerized import value`.
6. **Bands:** repeat Sheet 1 steps 4–10 with this data source's `window_band`: Rows, Maximum, Dual Axis, Bar, `#d9d8d3` at 45%, max size, fixed 0–1, hidden header, move marks to back.
7. **All** marks tab: `disruption_window` onto **Detail** and **Tooltip**.
8. Optional: label each line's last point (**Label → Line Ends**).
9. Title: `China imports by lane group (3-month average)`. Add a caption: "China-origin imports only."

Use the `_3mo_pct` columns to match the Q2 chart. The monthly `_pct` columns are there if you want the noisier raw series.

---

## 3. Sheet "Port map": symbol map from lat/lon, no geocoding

1. Data source: `port_map_tableau`. In the Data pane, right-click `lat` → **Geographic Role → Latitude**. Right-click `lon` → **Geographic Role → Longitude**. Their icons turn into globes.
2. **Columns:** `lon`. **Rows:** `lat`. Tableau draws a map. If the pills read `SUM(...)`, right-click each → **Measure → Average**. With one row per port it makes no difference, but AVG is the safe default.
3. **Detail:** `port`. This splits the single dot into 9 marks.
4. Mark type **Shape**. **Shape:** `dipped` → Edit Shapes: `Yes` = filled circle, `No` = open circle. Charleston and Houston never fell below their 2019 level, so they get open rings, as on the matplotlib map.
5. **Color:** `lane_group` → `Pacific-direct` `#2a78d6`, `Panama-dependent` `#eb6834`.
6. **Size:** `map_marker_size`. Size legend → Edit Sizes → **From zero**, so area stays proportional. `map_marker_size` equals `slump_points` (points below 2019 at the 2022–23 low), except the no-dip ports, which are set to 1 so they stay visible.
7. **Label:** `port` and `trough_index`. Edit the label to `<port>  <SUM(trough_index)>`.
8. **Tooltip:** `slump_points`, `trough_month`, `months_to_recover`, `latest_index`, `lalb_backlog_peak_ships`, `lalb_backlog_peak_month`, `savannah_backlog_peak_ships`, and `savannah_backlog_peak_month`. The backlog columns are blank except for the LA, Long Beach (LA-LB combined) and Savannah rows, which are the only port-level backlogs BTS publishes.
9. **Map → Background Maps → Light.** **Map → Map Layers:** washout about 30%, untick Country/Region Names. Zoom to the lower 48, then **Map → Map Options** → untick "Allow pan and zoom" if you want it fixed.
10. Los Angeles and Long Beach sit about 8 km apart, so their circles overlap at national zoom. Either leave it (the tooltip separates them), or add a caption: "LA and Long Beach overlap; hover to see each."
11. Title: `2022–23 import slump by port`. Caption: "Circle area = points below 2019 at the 2022–23 low, a per-port proxy. BTS reports berth backlogs only for LA + Long Beach combined, Savannah, and all other ports."

This map has no dates, so the disruption-window filter action doesn't apply to it (see step 5).

---

## 4. Sheet "Port series": backlog or throughput, one metric at a time

1. Data source: `port_series_tableau`. **Columns:** `date` as continuous month. **Rows:** `value`.
2. **Filters:** `metric_name` → pick `Loaded imports index`. Right-click the filter pill → **Show Filter**, and set the card to **Single Value (list)**. Readers then switch between `Loaded imports index` and `Ships awaiting a berth`.
3. **Detail:** `port_or_group`. Then **Color:** `lane_group` → `Pacific-direct` `#2a78d6`, `Panama-dependent` `#eb6834`, `All Other Ports` `#8a8984`. Each port or group gets its own line, colored by lane, as in Q3.
4. **Label:** `port_or_group` → Label options → **Line Ends**, so lines are direct-labeled.
5. **Bands:** Sheet 1 steps 4–10 with this source's `window_band`. Use **Maximum**, not Sum, here. Each month has up to 9 rows (one per port), so `SUM(window_band)` would stack to 9.
6. **All** marks tab: `disruption_window` onto **Detail** and **Tooltip**.
7. Title: click **Title → Insert → `metric_name`**, so the title follows the selected metric. Add `metric_units` to the caption the same way.
8. Two data gaps to know: berth counts start Jul 2021 and are missing for Oct 2025. The loaded-import index ends Jul 2026, and Charleston's Jul 2026 value is missing. If Tableau shows a "nulls" indicator, right-click it → **Hide Indicator**.

For the throughput view, a reference line at **Constant `100`** (the 2019 level) helps, as in Q3. Tableau shows it for both metrics, so add it only if you'll mostly show throughput.

---

## 5. Dashboard and filter action

**Layout**

1. **Dashboard → New Dashboard.** Size: **Fixed size, 1280 × 720**, the same as the pitch deck.
2. Drag in a **Horizontal** container. Into its left side drag a **Vertical** container, and drop in **GSCPI**, **Lane share**, and **Port series**, top to bottom. They share the same month axis, so readers can scan down one date.
3. Into the right side drag **Port map**, and below it the `metric_name` filter card (it appears automatically with Port series; move it).
4. Set the left column to about 62% of the width. Hide the sheet titles that repeat the dashboard title, and keep the window annotations on GSCPI only.
5. Dashboard title: `Global supply chain resilience, Jan 2019 – Sep 2026`.

**Filter action on `disruption_window`**

6. **Dashboard → Actions → Add Action → Filter.**
   - Name: `Filter by disruption window`.
   - Source Sheets: **GSCPI** only. Run action on: **Select**.
   - Target Sheets: **Lane share** and **Port series**. Untick **Port map**, which has no `disruption_window`.
   - Clearing the selection will: **Show all values**.
   - Filter: **Selected Fields** → **Add Filter**:
     - Source field `disruption_window` (gscpi_tableau) → Target data source `lane_share_tableau`, target field `disruption_window`.
     - Add a second row: source `disruption_window` → target data source `port_series_tableau`, target field `disruption_window`.
   - OK.
7. Test it: click a West Coast band on GSCPI. Lane share and Port series should narrow to Jan 2021 – Dec 2022. Click empty space to reset.

**What the action does with the overlap.** The window label is a single value per month, so clicking a Panama-only month keeps only Panama-only months (Jun–Oct 2023), and the overlap months have their own label. To show a whole window including the overlap, **Ctrl-click** a band month from each part (for Panama: one Panama-only month plus one overlap month). Alternatively, add `in_panama` / `in_red` as quick filters (show filter, Single Value list, select 1) instead of using the action.

---

## 6. Story

1. **Story → New Story.** Size: **Fixed 1280 × 800** (the extra height holds the navigator).
2. Drag the dashboard onto the story. Caption point 1: **Four disruptions on one timeline**. Leave nothing selected.
3. Click **Duplicate**. On the new point, click a West Coast band on GSCPI, then click **Update** above the caption. Caption: **West Coast congestion: cargo shifted east**.
4. Duplicate again. Ctrl-click a Panama-only month, an overlap month, and a Red Sea-only month → **Update**. Caption: **Panama drought and Red Sea: small westward drift**.
5. Duplicate again. Click a 2026 band → **Update**. Caption: **2026: pressure up, ports clear**.
6. Optional fifth point: the dashboard with the Port map tooltip open on Sea-Tac. Caption: **Pacific ports slumped hardest; Sea-Tac hasn't recovered**.

Keep the captions close to the findings in the q1–q4 READMEs. In particular, the Panama drought alone left the lane share flat; the westward drop came during the Red Sea window.

---

## About the .twbx

`tableau/supply_chain_resilience.twbx` is generated by `tableau/build_twbx.py`, which also writes the unzipped `supply_chain_resilience.twb` for review. It defines the same four sheets, the dashboard, the filter action, and a four-point story, packaged with the CSVs.

**It is confirmed broken, not just untested.** Tableau Desktop refuses to load it with error D2E8DA72. The `reference-line` elements fail the workbook schema (the element and all its attributes are undeclared), and so does the storyboard `window` element (`'storyboard'` isn't an allowed window class, and its required child elements are missing). The file is kept only as a record of the attempt. Don't use it or try to repair it; build from this guide.

The script's offline checks did pass: well-formed XML, every field declared in its data source, every named sheet present, and packaged CSV paths that resolve. That shows those checks can't catch schema errors, so a passing run of `build_twbx.py` says nothing about whether Tableau will load the file.
