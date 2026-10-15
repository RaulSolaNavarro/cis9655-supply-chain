# Global Supply Chain Resilience & Freight Disruption

CIS 9655 (Data Visualization): team final project.

## Research question

How have major disruptions (Red Sea rerouting, the Panama Canal drought, port congestion) affected freight cost pressure and trade volumes, and which lanes and regions have been more resilient?

| Folder | Sub-question | Primary data |
|---|---|---|
| [`q1-pressure/`](q1-pressure/) | How has the NY Fed GSCPI moved from pre-pandemic through these disruptions, and how do the spikes compare in size and duration? | NY Fed GSCPI |
| [`q2-trade-volume/`](q2-trade-volume/) | How have US trade volumes with key partners and regions shifted during the disruption windows (Asia/Red Sea, Latin America/Panama)? | Census international trade API |
| [`q3-ports/`](q3-ports/) | Which US ports saw the worst congestion, and which recovered fastest? | BTS Supply Chain & Freight Indicators |
| [`q4-synthesis/`](q4-synthesis/) | Combining Q1–Q3, which lanes came out more resilient, and why? | Outputs of Q1–Q3 |

## Project plan (team decisions, Oct 2026)

- **Framing:** centered on the ongoing 2026 disruption, with the 2021–2024 events (pandemic congestion, Red Sea, Panama drought) as comparison episodes.
- **Shared timeline:** monthly, **January 2019 through the latest available month**, across all three sources. Weekly BTS series get rolled up to monthly.
- **Q2 lane definition:** trade by US port, from the Census `imports/porths` endpoint. For imports, Census defines the port as the **port of unlading** (where the ship or plane is unloaded), not where goods clear customs. If port-level data turns out to be unusable, fall back to country-level comparison (`imports/hs`).
- **Q3 port selection:** use the same ports Q2 ends up using.
- **Q4:** start building the combined chart skeleton now, in parallel with Q1–Q3, and fill it in as their outputs land.

## Repo layout

```
data/raw/          downloaded source files (git-ignored, recreate with scripts/)
data/processed/    cleaned, analysis-ready tables (committed)
scripts/           shared data download / validation scripts
q1-pressure/ … q4-synthesis/   per-question analysis, notebooks, figures
```

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
```

**Census API key** (needed for Q2). Get a free key at https://api.census.gov/data/key_signup.html. It's emailed to you, and you have to click the activation link before it works. Then:

```bash
cp .env.example .env   # then paste your key after CENSUS_API_KEY=
```

Never commit `.env`. Each teammate should use their own key.

## Validating the data sources

Each script pulls a sample, saves it to `data/raw/`, and prints the date range, columns, units, and missing values.

```bash
python scripts/validate_gscpi.py    # no key needed
python scripts/validate_bts.py      # no key needed
python scripts/validate_census.py   # needs CENSUS_API_KEY
python scripts/validate_census_porths.py [YYYY-MM] [CTY_CODE]   # imports by port, default 2026-01 China
```

## Data snapshots (`data/processed/`)

The CSVs in `data/processed/` are **frozen snapshots for exploration, not live data**. Each file name ends with the date it was pulled (e.g. `gscpi_2026-10-15.csv`), and the files are never updated in place. Use them to start exploring and charting without any setup or API key.

| File | Contents |
|---|---|
| `gscpi_<date>.csv` | Full GSCPI series: `date` (month-end), `value` (std. deviations from average) |
| `bts_port_indicators_<date>.csv` | The 7 port-related BTS indicators: `date, indicator, port_or_region, value, units, source` |
| `census_exports_all_hs_2013-04_<date>.csv` | The brief's example call: all US exports, Apr 2013, every HS level (filter on `hs_level`) |
| `census_imports_china_hs2_<date>.csv` | Monthly US imports from China by HS2 chapter, Jan 2013 onward |
| `census_exports_mexico_hs2_<date>.csv` | Monthly US exports to Mexico by HS2 chapter, Jan 2013 onward |
| `census_porths_5700_lanes_<date>.csv` | Monthly US imports from China by port of unlading, all commodities, Jan 2019 onward. `bts_port` maps Census port codes to the 9 BTS ports, and `lane_group` is `Panama-dependent` (NY-NJ, Savannah, Port of VA, Charleston, Houston), `Pacific-direct` (LA, Long Beach, Oakland, Sea-Tac), or `Other`. The all-ports total row and `7070 LOW VALUE` are excluded. Both stay in the git-ignored raw pull (`data/raw/census_porths_5700_<start>_<end>.csv`). Rebuild with `python scripts/pull_census_porths_history.py [CTY_CODE] [START_YEAR]`. |

Census files keep monthly (`_MO`) fields only, renamed to `total_value_usd`, `vessel_value_usd`, `containerized_value_usd`, `air_value_usd`, `vessel_weight_kg`, and `shipment_count`. For imports, `total_value_usd` is the Census "general imports" value (`GEN_VAL_MO`).

**For a different country, a different date range, or fresher data, run the scripts yourself** with your own Census API key (see Setup). Run the `validate_*.py` scripts to pull, then `python scripts/export_snapshots.py` to write new dated snapshots. Don't overwrite or hand-edit the existing snapshot files.

## Data sources and known quirks

**NY Fed Global Supply Chain Pressure Index (GSCPI):** [download page](https://www.newyorkfed.org/research/policy/gscpi)
- Monthly, Jan 1998 to present. One global value per month, with no regional breakdown.
- Units: standard deviations from the historical average.
- The file is named `.xlsx` but is actually legacy `.xls`, so it needs the `xlrd` engine.
- Past values are revised with each release. Record the download date for any figures you publish.

**Census international trade API:** `https://api.census.gov/data/timeseries/intltrade/{exports,imports}/hs`
- Monthly, Jan 2013 to present, by country (`CTY_CODE`) and HS commodity code.
- Values are US dollars and weights are kilograms. There is no container or TEU count.
- Exports and imports use different field names (`E_COMMODITY`/`ALL_VAL_MO` vs `I_COMMODITY`/`GEN_VAL_MO`).
- `*_YR` fields are year-to-date cumulative. Use `*_MO` fields for monthly series.
- Requests without a key are rejected.
- Multi-year requests are slow (80–120s+) and can time out, so pull one year per request.
- Without a `COMM_LVL` filter, results mix HS2/4/6/10 rows. Always filter to one level before summing.
- Mexico trade is mostly truck/rail (vessel ≈ 10% of export value), so it isn't a Panama Canal lane.

**Census imports by port (`porths`):** `https://api.census.gov/data/timeseries/intltrade/imports/porths`
- One row per port × country × HS code × month. Commodity detail goes down to HS6, and `time` is required.
- Import port = **port of unlading**. Census may combine ports under one code to protect confidentiality.
- Every response includes a `PORT == "-"` "TOTAL FOR ALL PORTS" row. **Exclude it before summing**, or totals double.
- `7070 LOW VALUE` is a pseudo-port for low-value shipments, not a place. Some ports have no name (e.g. `1791`), and the list of ports varies month to month.
- All-commodity totals (`I_COMMODITY=-`) are fast: about 10s per month, about 16s per full year in one call. Per-port HS2 detail took 60–130s for a single month.
- Matching BTS port names to Census port codes: NY-NJ ≈ 1003 Newark + 1001 New York; Sea-Tac = 3001 Seattle + 3002 Tacoma; Port of VA ≈ 1401 Norfolk.

**BTS Supply Chain and Freight Indicators:** [data.bts.gov dataset `y5ut-ibwt`](https://data.bts.gov/d/y5ut-ibwt) (Socrata API, no key needed)
- Long format: `date, indicator, measure1 (port/region), value1, units`. Updated weekly.
- Monthly loaded/empty TEUs for 9 ports (LA, Long Beach, NY-NJ, Savannah, Houston, Virginia, Charleston, Oakland, Seattle-Tacoma) from 2019. These data lag by about 3 months.
- Weekly counts of ships waiting for a berth (LA-LB, Savannah, all others) and ships anchored by coast, from Jul 2021.
- Shanghai→LA spot rate ($/40ft box) and weekly containership capacity calling at US ports.
- The standalone BTS port datasets (`rd72-aq8r`, `iahn-a7j4`, `nfsh-p62e`) stop in 2022–2023. Don't use them for the disruption windows.
- The explore.dot.gov Tableau dashboards block scripted access (HTTP 403).
