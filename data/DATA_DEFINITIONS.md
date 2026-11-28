# Data definitions

CIS 9655 final project: Global Supply Chain Resilience.

This is the reference for every dataset, metric, and column in the repo. Use it to answer "where does this number come from, and what does it mean?" It covers the sources, the files, a dictionary of every column, how each metric is calculated, and the known quirks.

For the exploration that led to these choices, see the EDA notebook: [`eda/CIS9655_EDA_Supply_Chain_Resilience.ipynb`](../eda/CIS9655_EDA_Supply_Chain_Resilience.ipynb). For the short version in the deck, see slide 3 of the [intro deck](https://raulsolanavarro.github.io/cis9655-supply-chain/).

**Contents**

1. [Sources at a glance](#1-sources-at-a-glance)
2. [The four disruption windows](#2-the-four-disruption-windows)
3. [Metric definitions](#3-metric-definitions)
4. [Lane groups and port mapping](#4-lane-groups-and-port-mapping)
5. [File dictionaries](#5-file-dictionaries)
6. [Source notes and known quirks](#6-source-notes-and-known-quirks)
7. [How the data flows through the repo](#7-how-the-data-flows-through-the-repo)
8. [Glossary](#8-glossary)
9. [Limitations](#9-limitations)

---

## 1. Sources at a glance

We use three sources for the analysis. Three more Census files were pulled during early validation and are kept for context only.

| Source | Publisher | What it measures | Frequency | Coverage in our files | Key needed? |
|---|---|---|---|---|---|
| **GSCPI** (Global Supply Chain Pressure Index) | Federal Reserve Bank of New York | One global score for supply chain pressure | Monthly | Jan 1998 to Sep 2026 | No |
| **BTS Supply Chain and Freight Indicators** (dataset `y5ut-ibwt`) | Bureau of Transportation Statistics (BTS), which compiles data from MARAD, USDA and US port authorities | Port volume, ships waiting, ships anchored, ship capacity, freight rate | Weekly and monthly (varies by indicator) | Jan 2019 to Oct 2026 | No |
| **Census international trade API, imports by port** (`imports/porths`) | US Census Bureau | Value of imports by US port of unlading, for one country | Monthly | Jan 2019 to Aug 2026 (China only) | Yes (free) |
| Census international trade API, imports by commodity (`imports/hs`) | US Census Bureau | China imports by HS2 product chapter | Monthly | Jan 2013 to Aug 2026 | Yes (free) |
| Census international trade API, exports by commodity (`exports/hs`) | US Census Bureau | Mexico exports by HS2 chapter; one-month all-country example | Monthly | Jan 2013 to Aug 2026 (Mexico); Apr 2013 only (example) | Yes (free) |
| Natural Earth | Natural Earth (public domain) | Map outlines (land, countries, US states) | Static | 1:110m scale, v5.1.2 | No |

**Where to get them**

- GSCPI: https://www.newyorkfed.org/research/policy/gscpi
- BTS dataset: https://data.bts.gov/d/y5ut-ibwt (Socrata API)
- Census API: https://api.census.gov/data/timeseries/intltrade (free key at https://api.census.gov/data/key_signup.html)
- Natural Earth: https://github.com/nvkelso/natural-earth-vector (tag v5.1.2)

**Snapshot date.** All processed files were pulled on **2026-10-15**, and the date is part of each file name. Snapshots are frozen and never edited in place.

---

## 2. The four disruption windows

Every chart, table and Tableau view marks the same four windows. They are defined once, in `q1-pressure/build_gscpi_chart.py` (`WINDOWS`), and reused everywhere.

| # | Window | First month | Last month | Notes |
|---|---|---|---|---|
| 1 | West Coast port congestion | 2021-01 | 2022-12 | Pandemic-era backlog at LA-Long Beach |
| 2 | Panama Canal drought | 2023-06 | 2024-05 | Reduced canal transits |
| 3 | Red Sea / Suez rerouting | 2023-11 | 2024-12 | Overlaps window 2 from Nov 2023 to May 2024 |
| 4 | Renewed 2026 pressure | 2026-01 | latest month | Open-ended; GSCPI runs to Sep 2026, lane share to Aug 2026 |

In the Tableau CSVs each row carries a `disruption_window` label (overlap months show both names joined by " + ") and one 0/1 flag per window: `in_west`, `in_panama`, `in_red`, `in_renewed`.

---

## 3. Metric definitions

These are the five measures the Story uses, plus the supporting ones. Each entry gives the plain meaning, the exact calculation, the source fields, and the main caution.

### 3.1 Pressure score (GSCPI)

| | |
|---|---|
| **Plain meaning** | How stressed global supply chains are in a given month. |
| **Units** | Standard deviations from the index's own long-run average. 0 is an average month. +1 is clearly stressed (our threshold, `ELEVATED = 1.0`). |
| **Source field** | `value` in `gscpi_<date>.csv` (the NY Fed's "GSCPI Monthly Data" sheet). |
| **Calculation** | None. We use the published value as is, from Jan 2019 onward, with each date moved to the first of its month so it lines up with the other series. |
| **Built from** | The NY Fed combines shipping-cost measures and manufacturing-survey measures from several economies into one number. The input sources listed in the file are the Bureau of Labor Statistics, Harper Petersen, the Baltic Exchange, IHS Markit, the Institute for Supply Management, Haver Analytics and Refinitiv. See the NY Fed page for the method. |
| **Caution** | One global value per month, no regional split. Past values are revised with each release, so record the download date. |

### 3.2 Lane share (also "route share")

| | |
|---|---|
| **Plain meaning** | Of all China-origin cargo that arrives in US ports in shipping containers, what percent lands at ports on the Pacific-direct lane versus ports on the Panama-dependent lane. |
| **Units** | Percent of all China containerized import value, by month. |
| **Source fields** | `containerized_value_usd` and `lane_group` in `census_porths_5700_lanes_<date>.csv`. |
| **Calculation** | For each month: (1) add up `containerized_value_usd` for each of the three groups (Pacific-direct, Panama-dependent, Other); (2) divide each group by the month's total across all three groups; (3) multiply by 100. The charted line is the **3-month rolling average** of that share. The faint line behind it is the raw month. |
| **Why containerized value** | Total value includes air freight (about 29% of value on average) and non-container ocean cargo. Containerized value is the closest field to boxes crossing the ocean. |
| **Coverage** | The nine mapped ports carry about 93% of China's containerized import value (Pacific-direct about 62%, Panama-dependent about 31%, Other about 7%). The two lines add to about 93%, not 100%. |
| **Shift in a window** | `change_pp` = average share over the window's last 3 months minus the average over the 3 months before the window starts, in percentage points. Positive means cargo moved toward East and Gulf ports. |
| **Caution** | China-origin cargo only. Census values are customs values, which do not include freight or insurance. |

### 3.3 Loaded imports index (port volume)

| | |
|---|---|
| **Plain meaning** | How busy a port is with import containers, compared with that same port in 2019. |
| **Units** | Index. 100 equals the port's own 2019 monthly average. 80 means 20% below 2019. |
| **Source fields** | `value` where `indicator` is "Loaded Import Containers at Select U.S. Ports in TEUs", by `port_or_region`, in `bts_port_indicators_<date>.csv`. |
| **Calculation** | For each port: monthly TEUs divided by that port's 2019 monthly average, times 100, then a **3-month rolling average** (`min_periods=2`, so the first months still show). |
| **Trough** | The lowest index value between Jul 2022 and Dec 2023. |
| **Months to recover** | Months from the trough until the index first returns to 100 or higher. Zero if the port never fell below 100 in the search period. |
| **Caution** | A fall in volume is not the same as congestion. The 2023 slump also reflects weaker import demand. BTS publishes port TEUs with about a 3-month lag (latest month is Jul 2026). |

### 3.4 Ships waiting for a berth

| | |
|---|---|
| **Plain meaning** | Container ships that have arrived at a US port area and are waiting for a berth to open. A direct measure of a queue. |
| **Units** | Number of vessels, as a monthly mean of weekly readings. |
| **Source fields** | `value` where `indicator` is "Number of Containerships Awaiting Berths at all U.S. Ports", for `port_or_region` of "LA-LB", "Savannah" or "All Other Ports". |
| **Calculation** | Average the weekly readings within each calendar month. A trailing month is dropped if the last weekly reading is more than 7 days before month end. |
| **Excluded** | The "All U.S. Container Ports" total, so a total is never added to its own parts. |
| **Peak and recovery** | `peak_ships` and `peak_month` are the highest monthly mean. `cleared_month` is the first month after the peak below 25% of the peak (`CLEARED_FRACTION = 0.25`). |
| **Caution** | Starts in Jul 2021, so it cannot describe earlier months. Only three groups are published, so no other individual port has a backlog figure. October 2025 has no readings and shows as a gap. |

### 3.5 Shanghai to Los Angeles freight rate

| | |
|---|---|
| **Plain meaning** | The spot price to ship one 40-foot container from Shanghai to Los Angeles. |
| **Units** | US dollars per 40-foot container. |
| **Source field** | `value` where `indicator` is "Freight Rates in $ per 40ft Container from Shanghai to LA". Originally from Drewry via USDA AMS. |
| **Calculation** | None. We use the monthly value as published (Feb 2020 to Sep 2026). |
| **Lag correlation** | Pearson r between the rate at month *t* minus *lag* and the Panama-dependent share at month *t*. Computed for lags 0 to 12. The headline uses a 6-month lag. |
| **Caution** | The six-month correlation (0.48) is driven by 2021 to 2022 (0.82 through 2022, 0.09 from 2023). The series are smooth and trending, so the observations are not independent and we did not test significance. |

### 3.6 Supporting indicators

These are in the BTS file but are not used in the Story.

| Indicator | Meaning | Frequency | Place split |
|---|---|---|---|
| Loaded Export Containers at Select U.S. Ports in TEUs | Full export boxes leaving, by port | Monthly | 9 ports |
| Empty Export Containers at Select U.S. Ports in TEUs | Empty boxes sent back out, by port | Monthly | 9 ports |
| Number of Containerships Anchored off U.S. Ports | Ships anchored off the coast | Weekly | East, Gulf, West |
| Capacity of Containerships Calling at U.S. Ports (in TEUs) | Total carrying capacity of ships arriving | Weekly | None (system-wide) |

### 3.7 Episode scorecard (Q4)

One row per disruption window, built from the Q1 to Q3 stats files.

| Column | Meaning | Source |
|---|---|---|
| `peak_gscpi` | Highest pressure score in the window | `q1-pressure/gscpi_window_stats.csv` |
| `share_change_pp` | Change in Panama-dependent share, in percentage points | `q2-trade-volume/lane_share_window_stats.csv` |
| `lalb_ships_waiting_mean` | Average ships waiting at LA-Long Beach during the window | `q3-ports/port_backlog_stats.csv` |
| `cargo_moved` | "East" if `share_change_pp` is +0.5 or more, "West" if it is -0.5 or less, otherwise "No change" | Derived (`NO_CHANGE_PP = 0.5`) |

---

## 4. Lane groups and port mapping

BTS reports volumes for nine named ports. Census reports by its own port codes. The table maps one to the other and assigns each port to a lane group. The mapping lives in `scripts/pull_census_porths_history.py` (`BTS_PORTS` and `LANES`).

| Lane group | BTS port | Census port code(s) | Why this lane |
|---|---|---|---|
| **Pacific-direct** | Los Angeles | 2704 | One short crossing; reached directly from Asia |
| | Long Beach | 2709 | Same |
| | Oakland | 2811 | Same |
| | Sea-Tac (Seattle-Tacoma) | 3001 Seattle, 3002 Tacoma | Same |
| **Panama-dependent** | NY-NJ | 1003 Newark, 1001 New York | Asia cargo reaches East and Gulf ports through the Panama Canal (or Suez) |
| | Savannah | 1703 | Same |
| | Port of VA | 1401 Norfolk | Same |
| | Charleston | 1601 | Same |
| | Houston | 5301 | Same |
| **Other** | Every other Census port | all remaining codes | Not mapped; includes small ports and inland points |

Two BTS ports combine two Census codes. Their values are added together.

**Approximate port locations** (for maps only) are in `scripts/port_locations.py`. They are good to a few kilometers.

---

## 5. File dictionaries

### 5.1 Processed snapshots (`data/processed/`)

Frozen, analysis-ready CSVs. File names end with the pull date.

#### `gscpi_2026-10-15.csv` (345 rows)

| Column | Type | Meaning |
|---|---|---|
| `date` | date | Month-end date (for example 2026-09-30). |
| `value` | number | GSCPI, in standard deviations from the average. |

#### `bts_port_indicators_2026-10-15.csv` (4,930 rows)

Long format: one row per date, indicator and place.

| Column | Type | Meaning |
|---|---|---|
| `date` | date | Observation date. Weekly series use the week date; monthly series use the first of the month. |
| `indicator` | text | What is measured. Seven values (see 3.4 to 3.6). |
| `port_or_region` | text | Where. Empty for system-wide indicators (capacity, freight rate). Values include the nine ports, "LA-LB", "Savannah", "All Other Ports", "All U.S. Container Ports", and the coasts "East", "Gulf", "West". |
| `value` | number | The measurement, in the units below. |
| `units` | text | "TEUs", "Number of vessels", or "Dollars per 40ft box". |
| `source` | text | The agency that produced the indicator. |

Indicator coverage:

| Indicator | Rows | First | Last | Cadence | Source |
|---|---|---|---|---|---|
| Loaded Import Containers (TEUs) | 818 | 2019-01 | 2026-07 | Monthly | BTS analysis of TEU data published by US ports |
| Loaded Export Containers (TEUs) | 818 | 2019-01 | 2026-07 | Monthly | Same |
| Empty Export Containers (TEUs) | 818 | 2019-01 | 2026-07 | Monthly | Same |
| Containerships Awaiting Berths | 1,212 | 2021-07-27 | 2026-10-13 | Weekly | MARAD Office of Policy and Plans and the Marine Exchange of Southern California |
| Containerships Anchored | 780 | 2021-07-27 | 2026-10-13 | Weekly | MARAD analysis of IHS AIS live data |
| Capacity of Containerships Calling (TEUs) | 404 | 2019-01-06 | 2026-09-27 | Weekly | MARAD analysis of CBP vessel movement data |
| Freight Rate, Shanghai to LA | 80 | 2020-02 | 2026-09 | Monthly | USDA AMS, from Drewry Container Freight Rate Insight |

Zero values (165 rows) are real readings of an empty queue, not errors. There are no negative values and no duplicates.

#### `census_porths_5700_lanes_2026-10-15.csv` (24,000 rows)

China (country code 5700) imports, one row per month and US port of unlading, all commodities combined. The all-ports total row and the "7070 LOW VALUE" pseudo-port are removed.

| Column | Type | Meaning |
|---|---|---|
| `month` | text | Month, formatted YYYY-MM. 92 months, 2019-01 to 2026-08. |
| `port_code` | integer | Census port code. 361 distinct codes. |
| `port_name` | text | Census port name (for example "LOS ANGELES, CA"). Empty for 72 rows. |
| `bts_port` | text | The matching BTS port name, only for the nine mapped ports. Empty otherwise. |
| `lane_group` | text | "Pacific-direct", "Panama-dependent" or "Other". |
| `country_name` | text | Always "CHINA". |
| `total_value_usd` | integer | Census "general imports" value, US dollars. All modes combined (`GEN_VAL_MO`). |
| `vessel_value_usd` | integer | Value that arrived by vessel (`VES_VAL_MO`). |
| `containerized_value_usd` | integer | Value of containerized vessel cargo (`CNT_VAL_MO`). A subset of vessel value. **Used for lane share.** |
| `containerized_weight_kg` | integer | Shipping weight of containerized cargo, kilograms (`CNT_WGT_MO`). |
| `air_value_usd` | integer | Value that arrived by air (`AIR_VAL_MO`). |

#### `census_imports_china_hs2_2026-10-15.csv` (16,072 rows) and `census_exports_mexico_hs2_2026-10-15.csv` (15,908 rows)

Context only. One row per month and HS2 product chapter, 2013-01 to 2026-08.

| Column | Type | Meaning |
|---|---|---|
| `month` | text | YYYY-MM. |
| `country_code`, `country_name` | text | 5700 CHINA for imports; 2010 MEXICO for exports. |
| `hs_code` | integer | Two-digit product chapter (98 chapters for China, 97 for Mexico). Leading zeros are dropped (chapter 01 shows as 1). |
| `hs_level` | text | Always "HS2". |
| `total_value_usd` | integer | `GEN_VAL_MO` for imports, `ALL_VAL_MO` for exports. All modes. |
| `vessel_value_usd`, `containerized_value_usd`, `air_value_usd` | integer | Same meaning as above. |
| `vessel_weight_kg` | integer | Vessel shipping weight, kilograms (`VES_WGT_MO`). |

#### `census_exports_all_hs_2013-04_2026-10-15.csv` (15,254 rows)

The course brief's example call: all US exports, April 2013 only, at every HS level. Context only.

| Column | Type | Meaning |
|---|---|---|
| `month` | text | Always 2013-04. |
| `hs_code`, `hs_description`, `hs_level` | text | Commodity code, description, and level ("-" for the all-commodity total, then HS2, HS4, HS6, HS10). **Filter to one level before summing.** |
| `total_value_usd`, `vessel_value_usd`, `air_value_usd` | integer | US dollars (`ALL_VAL_MO`, `VES_VAL_MO`, `AIR_VAL_MO`). |
| `shipment_count` | integer | Number of shipments (`CC_MO`). |

### 5.2 Raw downloads (`data/raw/`)

Source files as downloaded, kept so anyone can trace a number back.

| File | What it is | Notes |
|---|---|---|
| `gscpi_data.xls` | The NY Fed workbook | Named `.xlsx` on the site but really legacy `.xls`, so it needs the `xlrd` engine. Sheets: "GSCPI Overview" (banner, sources, how to cite) and "GSCPI Monthly Data". |
| `bts_port_indicators_sample.csv` | The seven BTS indicators, as pulled | Columns: `id, date, year, indicator, measure1, measure1_description, value1, units, source, note`. The processed file renames `measure1` to `port_or_region` and `value1` to `value`. |
| `census_porths_5700_2019-01_2026-08.csv` | China imports by port, untouched pull | Columns use Census field names: `PORT, PORT_NAME, CTY_NAME, GEN_VAL_MO, VES_VAL_MO, CNT_VAL_MO, CNT_WGT_MO, AIR_VAL_MO, time, CTY_CODE, I_COMMODITY`. Keeps the "TOTAL FOR ALL PORTS" row (`PORT == "-"`) and "7070 LOW VALUE", which the processed file removes. |
| `census_porths_5700_2026-01.csv` | One-month test pull (Jan 2026) | Used to validate the endpoint. |
| `census_sample_*.csv` | Early validation pulls | Brief example, China HS2 imports, Mexico HS2 exports. |
| `natural_earth/*.geojson` | Map outlines | Land, countries, US states. Public domain. |

### 5.3 Tableau-ready CSVs (`tableau/data/`)

Built by `tableau/build_tableau_data.py` from the same loader functions as the matplotlib charts, so the Tableau views match the figures. Window labels are precomputed, so Tableau needs no calculated fields.

Shared window columns on the first three tables: `disruption_window` (label, or blank), `in_west`, `in_panama`, `in_red`, `in_renewed` (1 or 0), and `window_band` (1 inside any window, blank outside; used to draw the gray shading).

| File | Rows | Columns | Notes |
|---|---|---|---|
| `gscpi_tableau.csv` | 93 | `date`, `gscpi_value`, plus window columns | Jan 2019 to Sep 2026. |
| `lane_share_tableau.csv` | 92 | `date`, `panama_dependent_share_pct`, `pacific_direct_share_pct`, `panama_dependent_share_3mo_pct`, `pacific_direct_share_3mo_pct`, plus window columns | The two `_3mo_` columns are the bold lines. |
| `port_series_tableau.csv` | 1,008 | `date`, `port_or_group`, `lane_group`, `metric_name`, `metric_units`, `value`, plus window columns | Long format with two metrics: "Ships awaiting a berth" (monthly mean) and "Loaded imports index" (3-month average, 2019 = 100). Missing months are kept as blank values. |
| `port_map_tableau.csv` | 9 | `port`, `lat`, `lon`, `lane_group`, `trough_index`, `trough_month`, `slump_points`, `map_marker_size`, `dipped`, `months_to_recover`, `latest_index`, `latest_month`, and backlog peak columns for LA-LB and Savannah | One row per port. `slump_points` is 100 minus the trough index (zero if the port never dipped). `map_marker_size` equals `slump_points`, or 1 for ports that never dipped, because Tableau cannot size a mark at 0. |
| `scorecard_tableau.csv` | 4 | `episode_order`, `episode`, `start`, `end`, `peak_gscpi`, `share_change_pp`, `lalb_ships_waiting_mean`, `cargo_moved`, `note` | The episode scorecard (3.7). |

**Colors** used everywhere: Pacific-direct and the pressure line `#2a78d6` (blue), Panama-dependent `#eb6834` (orange), All Other Ports `#8a8984` (gray), window bands `#d9d8d3`.

### 5.4 Per-question stats files

| File | One row per | Key columns |
|---|---|---|
| `q1-pressure/gscpi_window_stats.csv` | Window | `months`, `peak`, `peak_month`, `mean`, `months_above_0`, `months_above_1` |
| `q2-trade-volume/lane_share_window_stats.csv` | Window | `panama_share_before`, `panama_share_end`, `change_pp`, `panama_share_mean`, `vs_2019_pp` |
| `q3-ports/port_backlog_stats.csv` | Backlog group | `peak_ships`, `peak_month`, `cleared_month`, `months_to_clear`, `mean_<window>`, `latest_ships` |
| `q3-ports/port_throughput_stats.csv` | Port | `congestion_window_peak`, `trough_index`, `trough_month`, `recovered_month`, `months_to_recover`, `latest_index` |
| `q4-synthesis/episode_scorecard.csv` | Window | See 3.7 |
| `q4-synthesis/lag_correlations.csv` | Driver and lag (0 to 12) | `n`, `r`, plus `r_through_2022`, `r_2023_on` and their `n` at the 6-month lag |

---

## 6. Source notes and known quirks

**GSCPI**

- Monthly, Jan 1998 to present. One global value per month, no regional breakdown.
- The download is named `.xlsx` but is a legacy `.xls` file. Use the `xlrd` engine.
- The data sheet has a few banner rows below the table. Keep only rows where both the date and the value parse.
- Past values are revised with each release. Record the download date for any published figure.

**Census trade API (all endpoints)**

- Monthly, Jan 2013 to present. Values are US dollars and weights are kilograms. There is no container or TEU count.
- Every field comes back as text. Convert to numbers before summing.
- Exports and imports use different field names (`E_COMMODITY` and `ALL_VAL_MO` for exports, `I_COMMODITY` and `GEN_VAL_MO` for imports).
- Fields ending `_YR` are year-to-date running totals. Use the `_MO` fields for a monthly series.
- Requests without a key are rejected. A key that has not been activated returns a redirect or an HTML page instead of JSON.
- Multi-year requests are slow (80 to 120 seconds or more) and can time out. Pull one year per request.
- Without a `COMM_LVL` filter, results mix HS2, HS4, HS6 and HS10 rows. Filter to one level before summing.
- Mexico trade is mostly truck and rail (vessel is about 11% of export value), so it is not a Panama Canal lane.

**Census imports by port (`porths`)**

- One row per port, country, HS code and month. `time` is required.
- The import port is the **port of unlading**, where the ship or plane is unloaded, not where goods clear customs.
- Census may combine ports under one code to protect confidentiality.
- Every response includes a `PORT == "-"` "TOTAL FOR ALL PORTS" row. **Exclude it before summing**, or totals double. The pull script checks that the ports sum to this total before dropping it.
- `7070 LOW VALUE` is a pseudo-port for low-value shipments, not a place.
- Some ports have no name (for example `1791`), and the list of ports varies month to month.
- All-commodity totals (`I_COMMODITY=-`) are fast, about 10 seconds a month. Per-port detail at HS2 took 60 to 130 seconds for one month.

**BTS Supply Chain and Freight Indicators**

- Long format. Updated weekly through the Socrata API (`https://data.bts.gov/resource/y5ut-ibwt.json`), no key needed.
- Monthly port TEUs lag by about three months, so the newest port volume is older than the newest ships-waiting reading.
- Weekly ships-waiting and anchored series start in Jul 2021.
- No weekly readings exist for October 2025. The gap is kept as a break in the line.
- The standalone BTS port datasets (`rd72-aq8r`, `iahn-a7j4`, `nfsh-p62e`) stop in 2022 or 2023 and are not used.
- The explore.dot.gov dashboards block scripted access (HTTP 403).

**Natural Earth**

- Map outlines only, at 1:110m scale. `scripts/map_outlines.py` reads them.

---

## 7. How the data flows through the repo

```
Source websites and APIs
   |  scripts/validate_gscpi.py, validate_bts.py, validate_census.py,
   |  validate_census_porths.py, pull_census_porths_history.py
   v
data/raw/                    untouched downloads
   |  scripts/export_snapshots.py, pull_census_porths_history.py
   v
data/processed/              cleaned, dated, frozen CSVs
   |  q1-pressure/ ... q4-synthesis/ build_*.py
   v
q1-q4 folders                charts (PNG) and stats (CSV)
   |  tableau/build_tableau_data.py
   v
tableau/data/                Tableau-ready CSVs
   v
tableau/team/*.twbx          Tableau workbook and Story
```

**To refresh the data** (needs your own free Census key in `.env`; see the README):

```bash
python scripts/validate_gscpi.py
python scripts/validate_bts.py
python scripts/validate_census.py
python scripts/pull_census_porths_history.py          # China by port, from 2019
python scripts/export_snapshots.py                    # writes new dated snapshots
```

Do not overwrite or hand-edit the existing dated snapshots. Write new ones and point the build scripts at them. Each build script reads the newest file that matches its pattern.

---

## 8. Glossary

| Term | Meaning |
|---|---|
| **GSCPI** | Global Supply Chain Pressure Index, from the New York Fed. |
| **Standard deviation** | A measure of how far a value sits from the average. The GSCPI is scaled so its history has a standard deviation near 1. |
| **TEU** | Twenty-foot equivalent unit. One 20-foot container is 1 TEU; a 40-foot container is 2 TEU. |
| **Containerized** | Cargo that arrives inside a shipping container. |
| **HS code (HS2, HS4, HS6, HS10)** | Harmonized System product code. The number is how many digits are kept: HS2 is a broad chapter, HS10 is a specific product. |
| **Port of unlading** | The US port where cargo is taken off the ship or plane. |
| **General imports** | The Census measure of total imports, valued at customs value (does not include freight or insurance). |
| **Lane** | A route group from China to the US. We use two: Pacific-direct and Panama-dependent. |
| **Pacific-direct** | Ports on the US West Coast, reached by one crossing of the Pacific. |
| **Panama-dependent** | Ports on the East and Gulf coasts, reached from Asia through the Panama Canal (or Suez). |
| **Berth** | A dock space where a ship loads and unloads. A ship "awaiting a berth" is queuing. |
| **Index (2019 = 100)** | A series divided by its own 2019 average and multiplied by 100, so different-sized ports share one scale. |
| **3-month rolling average** | The average of the current month and the two before it. Smooths timing noise. |
| **Percentage point (pp)** | The difference between two percentages. Moving from 30% to 32% is 2 pp. |
| **Lag** | How many months one series leads another when we compare them. |
| **Pearson r** | A number from -1 to +1 showing how closely two series move together. It does not show cause. |
| **MARAD** | US Maritime Administration. |
| **AIS** | Automatic Identification System, the ship-tracking signal. |

---

## 9. Limitations

- **Four episodes support a pattern, not proof.** Two windows (Panama and Red Sea) overlap and cannot be separated.
- **China-origin cargo only.** Other origins may behave differently. Mexico, the largest US source, moves mostly by truck and rail.
- **Nine ports.** They carry about 93% of China's containerized import value, so the lane share is a good but not complete picture.
- **Congestion is only measured directly at LA-Long Beach and Savannah.** BTS publishes ships waiting for three groups only, and only from Jul 2021.
- **Volume is not congestion.** A drop in port TEUs can come from weaker demand.
- **Revisions.** GSCPI, BTS and Census figures are revised over time. Our snapshots are frozen at 2026-10-15.
- **Correlation is not cause.** Demand, tariffs and carrier decisions also move these series.
- **Freight rate lead is fragile.** The six-month relationship comes almost entirely from 2021 to 2022.

**How to cite the sources**

- Federal Reserve Bank of New York, Global Supply Chain Pressure Index, https://www.newyorkfed.org/research/gscpi.html
- US Bureau of Transportation Statistics, Supply Chain and Freight Indicators, https://data.bts.gov/d/y5ut-ibwt
- US Census Bureau, International Trade API (timeseries/intltrade), https://api.census.gov/data/timeseries/intltrade
