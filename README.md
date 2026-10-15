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
```

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

**BTS Supply Chain and Freight Indicators:** [data.bts.gov dataset `y5ut-ibwt`](https://data.bts.gov/d/y5ut-ibwt) (Socrata API, no key needed)
- Long format: `date, indicator, measure1 (port/region), value1, units`. Updated weekly.
- Monthly loaded/empty TEUs for 9 ports (LA, Long Beach, NY-NJ, Savannah, Houston, Virginia, Charleston, Oakland, Seattle-Tacoma) from 2019. These data lag by about 3 months.
- Weekly counts of ships waiting for a berth (LA-LB, Savannah, all others) and ships anchored by coast, from Jul 2021.
- Shanghai→LA spot rate ($/40ft box) and weekly containership capacity calling at US ports.
- The standalone BTS port datasets (`rd72-aq8r`, `iahn-a7j4`, `nfsh-p62e`) stop in 2022–2023. Don't use them for the disruption windows.
- The explore.dot.gov Tableau dashboards block scripted access (HTTP 403).
