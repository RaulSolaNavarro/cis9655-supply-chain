# Global Supply Chain Resilience & Freight Disruption

CIS 9655 (Data Visualization): team final project.

## Start here

**Present and review**

| What | Link | What is there |
|---|---|---|
| Tableau Story (main deliverable) | https://public.tableau.com/views/SupplyChainResilience-Team/Story | The five-point Tableau Public Story we present. The workbook with its data is [tableau/team/Supply Chain Resilience - Team.twbx](tableau/team/Supply%20Chain%20Resilience%20-%20Team.twbx). |
| Intro deck (web) | https://raulsolanavarro.github.io/cis9655-supply-chain/ | The short deck that sets up the question, the data definitions and the routes before the Story, then closes with our answer. Press S for speaker notes, F for full screen. |
| Earlier pitch deck | https://raulsolanavarro.github.io/cis9655-supply-chain/pitch.html | The Oct 15 pitch, kept for history. |
| Speaker script | [presentation/final_presentation_script.md](presentation/final_presentation_script.md) | Raul's deck lines, the hand-offs, timing, click cues and the in-person checklist. |
| Tableau Story speaker notes | [presentation/story_speaker_notes.md](presentation/story_speaker_notes.md) | For each presenter: the analytical question, how the view answers it, the design decisions, numbers, and likely questions. |
| Plain-English FAQ | [presentation/plain_english_faq.md](presentation/plain_english_faq.md) | Plain answers to the questions we expect, with sources. |
| Q&A prep sheet | [presentation/qa_prep_sheet.md](presentation/qa_prep_sheet.md) | Key terms, data sources, how each metric is calculated, limitations, decisions, and likely questions. |
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
| Final workbook | [tableau/team/Supply Chain Resilience - Team.twbx](tableau/team/Supply%20Chain%20Resilience%20-%20Team.twbx) | The combined workbook: five sheets, five dashboards, and the Story. Data is embedded, so it opens with no setup. |
| Team start page | [tableau/team/README.md](tableau/team/README.md) | How the four-person Tableau build was split and combined. |
| Jason's guide | [tableau/team/01_jason_gscpi.md](tableau/team/01_jason_gscpi.md) | Pressure line with disruption bands. |
| Paven's guide | [tableau/team/02_paven_lane_share.md](tableau/team/02_paven_lane_share.md) | Two-line lane share chart. |
| Supriya's guide | [tableau/team/03_supriya_ports.md](tableau/team/03_supriya_ports.md) | Port map and port series. |
| Raul's guide | [tableau/team/04_raul_dashboard.md](tableau/team/04_raul_dashboard.md) | Combined dashboards and story. |
| Full build guide | [tableau/BUILD_GUIDE.md](tableau/BUILD_GUIDE.md) | The long reference version of all Tableau steps. |
| Tableau data | [tableau/data/](tableau/data/) | The four ready-to-use CSVs. |

**Data and code**

| What | Link | What is there |
|---|---|---|
| Data definitions | [data/DATA_DEFINITIONS.md](data/DATA_DEFINITIONS.md) | Every source, metric and column: what it means, how it is calculated, where it comes from, and the known quirks. Start here to understand the data. |
| Exploratory data analysis | [eda/CIS9655_EDA_Supply_Chain_Resilience.ipynb](eda/CIS9655_EDA_Supply_Chain_Resilience.ipynb) | Python notebook, commented line by line: data checks, distributions, lane share, ports, and the freight-rate lead. [Open in Colab](https://colab.research.google.com/github/RaulSolaNavarro/cis9655-supply-chain/blob/main/eda/CIS9655_EDA_Supply_Chain_Resilience.ipynb). No API key needed. |
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
data/DATA_DEFINITIONS.md   sources, metric definitions, and a column dictionary for every file
eda/               exploratory data analysis notebook (runs in Google Colab, reads the snapshots from GitHub)
scripts/           shared data download / validation scripts
q1-pressure/ … q4-synthesis/   per-question analysis, notebooks, figures
                   (q4-synthesis/ also holds episode_scorecard.png and rate_vs_share_scatter.png)
tableau/           Tableau-ready CSVs and BUILD_GUIDE.md (the long reference for rebuilding the views by hand)
tableau/team/      the final workbook (Supply Chain Resilience - Team.twbx), each teammate's own workbook and build guide, and a start page (README.md)
docs/index.html    the short intro deck that leads into the Tableau Story (reveal.js, served by GitHub Pages; press S for speaker notes)
docs/pitch.html    the earlier pitch deck, kept for history
docs/assets/       the images embedded in the intro and backup slides (copies of the q1–q4 figures)
presentation/      the full script with timing and speaker assignments, the Tableau team-build split, and the Q&A prep sheet
                   final_presentation_script.md   Raul's deck lines, hand-offs, timing and the in-person checklist
                   story_speaker_notes.md         per-person Tableau Story notes: question, answer, design decisions
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
| `census_porths_5700_lanes_<date>.csv` | Monthly US imports from China by port of unlading, all commodities, Jan 2019 onward. `bts_port` maps Census port codes to the 9 BTS ports, and `lane_group` is `Panama-dependent` (NY-NJ, Savannah, Port of VA, Charleston, Houston), `Pacific-direct` (LA, Long Beach, Oakland, Seattle-Tacoma), or `Other`. The all-ports total row and `7070 LOW VALUE` are excluded. Both stay in the raw pull (`data/raw/census_porths_5700_<start>_<end>.csv`). Rebuild with `python scripts/pull_census_porths_history.py [CTY_CODE] [START_YEAR]`. |

Census files keep monthly (`_MO`) fields only, renamed to `total_value_usd`, `vessel_value_usd`, `containerized_value_usd`, `air_value_usd`, `vessel_weight_kg`, and `shipment_count`. For imports, `total_value_usd` is the Census "general imports" value (`GEN_VAL_MO`).

**For a different country, a different date range, or fresher data, run the scripts yourself** with your own Census API key (see Setup). Run the `validate_*.py` scripts to pull, then `python scripts/export_snapshots.py` to write new dated snapshots. Don't overwrite or hand-edit the existing snapshot files.

## Data sources and known quirks

The full column dictionary, metric formulas and glossary are in [data/DATA_DEFINITIONS.md](data/DATA_DEFINITIONS.md). The notes below are the short version.

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
- Matching BTS port names to Census port codes: NY-NJ ≈ 1003 Newark + 1001 New York; Seattle-Tacoma = 3001 Seattle + 3002 Tacoma; Port of VA ≈ 1401 Norfolk.

**BTS Supply Chain and Freight Indicators:** [data.bts.gov dataset `y5ut-ibwt`](https://data.bts.gov/d/y5ut-ibwt) (Socrata API, no key needed)
- Long format: `date, indicator, measure1 (port/region), value1, units`. Updated weekly.
- Monthly loaded/empty TEUs for 9 ports (LA, Long Beach, NY-NJ, Savannah, Houston, Virginia, Charleston, Oakland, Seattle-Tacoma) from 2019. These data lag by about 3 months.
- Weekly counts of ships waiting for a berth (LA-LB, Savannah, all others) and ships anchored by coast, from Jul 2021.
- Shanghai→LA spot rate ($/40ft box) and weekly containership capacity calling at US ports.
- The standalone BTS port datasets (`rd72-aq8r`, `iahn-a7j4`, `nfsh-p62e`) stop in 2022–2023. Don't use them for the disruption windows.
- The explore.dot.gov Tableau dashboards block scripted access (HTTP 403).

**Natural Earth outlines (maps only):** 1:110m land, countries, and US states GeoJSON in `data/raw/natural_earth/`, from [nvkelso/natural-earth-vector](https://github.com/nvkelso/natural-earth-vector) tag v5.1.2 (public domain). `scripts/map_outlines.py` reads them, and `scripts/port_locations.py` holds approximate coordinates for the 9 BTS ports.
