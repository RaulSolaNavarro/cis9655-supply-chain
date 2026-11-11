# Global Supply Chain Resilience & Freight Disruption

CIS 9655 (Data Visualization): team final project.

## Start here

**Present and review**

| What | Link | What is there |
|---|---|---|
| Final presentation (web deck) | https://raulsolanavarro.github.io/cis9655-supply-chain/ | The 8-slide deck we present. Press S for speaker notes, F for full screen. |
| Earlier pitch deck | https://raulsolanavarro.github.io/cis9655-supply-chain/pitch.html | The Oct 15 pitch, kept for history. |
| Final presentation (Google Slides) | https://docs.google.com/presentation/d/1a68IT-oZYxsnWrZ2Whijz4o7LiLRtB-lV0DvrHOGjk8/edit | A Google Slides copy of the same deck, for the shared folder. |
| Speaker script | [presentation/final_presentation_script.md](presentation/final_presentation_script.md) | Who says what, with timing, plus the in-person checklist. |
| Plain-English FAQ | [presentation/plain_english_faq.md](presentation/plain_english_faq.md) | Plain answers to the questions we expect, with sources. |
| Q&A prep sheet | [presentation/qa_prep_sheet.md](presentation/qa_prep_sheet.md) | Answers to the professor's question types and likely audience questions. |
| Visualization decisions | [presentation/visualization_decisions.md](presentation/visualization_decisions.md) | Why each chart is drawn the way it is, in course vocabulary. |

**Analysis, one folder per question**

| What | Link | What is there |
|---|---|---|
| Q1 pressure | [q1-pressure/](q1-pressure/) | NY Fed pressure score by disruption window, chart, stats, method notes. |
| Q2 lanes | [q2-trade-volume/](q2-trade-volume/) | Share of China imports at West Coast versus East and Gulf ports. |
| Q3 ports | [q3-ports/](q3-ports/) | Ships waiting, port volume, and the port map. |
| Q4 synthesis | [q4-synthesis/](q4-synthesis/) | Route map, episode scorecard, stacked strips, and the shipping price scatter. |

**Tableau**

| What | Link | What is there |
|---|---|---|
| Team start page | [tableau/team/README.md](tableau/team/README.md) | Setup and publishing steps for the four-person Tableau build. |
| Jason's guide | [tableau/team/01_jason_gscpi.md](tableau/team/01_jason_gscpi.md) | Pressure line with disruption bands. |
| Paven's guide | [tableau/team/02_paven_lane_share.md](tableau/team/02_paven_lane_share.md) | Two-line lane share chart. |
| Supriya's guide | [tableau/team/03_supriya_ports.md](tableau/team/03_supriya_ports.md) | Port map and port series. |
| Raul's guide | [tableau/team/04_raul_dashboard.md](tableau/team/04_raul_dashboard.md) | Combined dashboard, filter action, and story. |
| Full build guide | [tableau/BUILD_GUIDE.md](tableau/BUILD_GUIDE.md) | The long reference version of all Tableau steps. |
| Tableau data | [tableau/data/](tableau/data/) | The four ready-to-use CSVs. |
| Tableau Public dashboard | Link added when published | The combined interactive dashboard. |

**Data and code**

| What | Link | What is there |
|---|---|---|
| Processed data snapshots | [data/processed/](data/processed/) | Frozen CSVs for exploring without an API key. |
| Raw data | [data/raw/](data/raw/) | Source downloads. |
| Scripts | [scripts/](scripts/) | Download, validation, and snapshot scripts. |
| Data sources and quirks | [Data sources and known quirks](#data-sources-and-known-quirks) | Where each dataset comes from and its gotchas. |

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
data/raw/          downloaded source files (committed, so EDA needs no API key; refresh with scripts/)
data/processed/    cleaned, analysis-ready tables (committed)
scripts/           shared data download / validation scripts
q1-pressure/ … q4-synthesis/   per-question analysis, notebooks, figures
                   (q4-synthesis/ also holds episode_scorecard.png and rate_vs_share_scatter.png)
tableau/           Tableau-ready CSVs, BUILD_GUIDE.md for building the workbook by hand, and a generated .twbx that is confirmed broken (Tableau won't load it)
tableau/team/      one Tableau build guide per teammate, plus a start page (README.md)
docs/index.html    the final presentation deck (reveal.js, served by GitHub Pages; press S for speaker notes)
docs/pitch.html    the earlier pitch deck, kept for history
docs/assets/       the chart and map images embedded in the final deck (copies of the q1–q4 figures)
presentation/      the full script with timing and speaker assignments, the Tableau team-build split, and the Q&A prep sheet
                   final_presentation_script.md   who says what on each slide, with timing and the in-person checklist
                   plain_english_faq.md           plain answers to the questions we expect
                   qa_prep_sheet.md               answers by question type
                   visualization_decisions.md     why each chart is drawn the way it is
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
| `census_porths_5700_lanes_<date>.csv` | Monthly US imports from China by port of unlading, all commodities, Jan 2019 onward. `bts_port` maps Census port codes to the 9 BTS ports, and `lane_group` is `Panama-dependent` (NY-NJ, Savannah, Port of VA, Charleston, Houston), `Pacific-direct` (LA, Long Beach, Oakland, Sea-Tac), or `Other`. The all-ports total row and `7070 LOW VALUE` are excluded. Both stay in the raw pull (`data/raw/census_porths_5700_<start>_<end>.csv`). Rebuild with `python scripts/pull_census_porths_history.py [CTY_CODE] [START_YEAR]`. |

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

**Natural Earth outlines (maps only):** 1:110m land, countries, and US states GeoJSON in `data/raw/natural_earth/`, from [nvkelso/natural-earth-vector](https://github.com/nvkelso/natural-earth-vector) tag v5.1.2 (public domain). `scripts/map_outlines.py` reads them, and `scripts/port_locations.py` holds approximate coordinates for the 9 BTS ports.
