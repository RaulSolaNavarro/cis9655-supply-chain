"""Validate BTS port data sources.

Main source: the BTS "Supply Chain and Freight Indicators" dataset on the
Open Data Catalog (Socrata id y5ut-ibwt). It is a long-format table
(one row per date x indicator x port/region) that is updated weekly and
covers 2019 to the present.

Also reports the date coverage of the older single-purpose port datasets on
data.bts.gov, and checks whether explore.dot.gov accepts scripted requests.

Usage:  python scripts/validate_bts.py
Output: data/raw/bts_port_indicators_sample.csv
"""
from pathlib import Path

import pandas as pd
import requests
import truststore

truststore.inject_into_ssl()  # trust the OS certificate store, not just certifi

SODA = "https://data.bts.gov/resource/{}.json"
INDICATORS_ID = "y5ut-ibwt"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Indicators in y5ut-ibwt relevant to port congestion / resilience (Q3)
PORT_INDICATORS = [
    "Loaded Import Containers at Select U.S. Ports in TEUs",
    "Loaded Export Containers at Select U.S. Ports in TEUs",
    "Empty Export Containers at Select U.S. Ports in TEUs",
    "Number of Containerships Awaiting Berths at all U.S. Ports",
    "Number of Containerships Anchored off U.S. Ports",
    "Capacity of Containerships Calling at U.S. Ports (in TEUs)",
    "Freight Rates in $ per 40ft Container from Shanghai to LA",
]

# Older standalone port datasets that turned up in the catalog search
LEGACY_DATASETS = {
    "rd72-aq8r": "Monthly TEU Data (9 ports)",
    "iahn-a7j4": "TEUs Handled by Select U.S. Container Ports",
    "nfsh-p62e": "Monthly Avg Container Vessel Dwell Times, Top 25 Ports",
    "5rpz-kgm9": "Port Data (annual, port profiles)",
    "sn74-xpkp": "Top 25 Container Ports by TEU (single year snapshot)",
}


def soda(dataset_id: str, **params) -> list[dict]:
    resp = requests.get(SODA.format(dataset_id), params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def check_indicators() -> None:
    print(f"=== Supply Chain and Freight Indicators ({INDICATORS_ID}) ===")
    meta = requests.get(f"https://data.bts.gov/api/views/{INDICATORS_ID}.json", timeout=60).json()
    print(f"Columns: {[c['fieldName'] + ':' + c['dataTypeName'] for c in meta['columns']]}")

    quoted = ", ".join("'" + i.replace("'", "''") + "'" for i in PORT_INDICATORS)
    rows = soda(INDICATORS_ID, **{"$where": f"indicator in ({quoted})", "$limit": 50000, "$order": "date"})
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df["value1"] = pd.to_numeric(df["value1"], errors="coerce")
    df.to_csv(RAW_DIR / "bts_port_indicators_sample.csv", index=False)
    print(f"Pulled {len(df):,} rows for {df['indicator'].nunique()} port-related indicators")

    summary = (df.groupby(["indicator", "measure1"], dropna=False)
                 .agg(start=("date", "min"), end=("date", "max"), n=("date", "size"),
                      units=("units", "first"), null_values=("value1", lambda s: s.isna().sum()))
                 .reset_index())
    # Infer cadence from the median gap between observations
    summary["cadence_days"] = (df.sort_values("date").groupby(["indicator", "measure1"], dropna=False)["date"]
                                 .apply(lambda s: s.diff().dt.days.median()).values)
    with pd.option_context("display.width", 250, "display.max_colwidth", 60):
        print(summary.to_string(index=False))

    teu = df[df["indicator"] == PORT_INDICATORS[0]]
    print("\nLoaded import TEUs, latest month per port:")
    latest = teu.sort_values("date").groupby("measure1").tail(1)
    print(latest[["measure1", "date", "value1"]].to_string(index=False))


def check_legacy() -> None:
    print("\n=== Older standalone port datasets on data.bts.gov ===")
    for ds_id, label in LEGACY_DATASETS.items():
        meta = requests.get(f"https://data.bts.gov/api/views/{ds_id}.json", timeout=60).json()
        n = soda(ds_id, **{"$select": "count(*) as n"})[0]["n"]
        cols = [c["fieldName"] for c in meta["columns"]]
        updated = pd.to_datetime(meta.get("rowsUpdatedAt"), unit="s")
        print(f"{ds_id}  {label}: {n} rows, last updated {updated:%Y-%m-%d}, columns={cols}")


def check_explore_dot_gov() -> None:
    print("\n=== explore.dot.gov (Tableau dashboards) ===")
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"}
    try:
        resp = requests.get("https://explore.dot.gov/", headers=ua, timeout=30)
        print(f"HTTP {resp.status_code} for scripted request"
              + (" -> blocked; dashboards are browser-only (manual export at best)" if resp.status_code == 403 else ""))
    except requests.RequestException as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    check_indicators()
    check_legacy()
    check_explore_dot_gov()
